from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.datastructures import MultiValueDict
from django.db import models
from PIL import Image , ImageOps
from io import BytesIO
from django.forms.widgets import HiddenInput
from django_otp.forms import OTPAuthenticationFormMixin
from django.contrib.auth.forms import AuthenticationForm
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.urls import  reverse
from .models import MyUsers


User =  get_user_model ()

class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs = {'class':'form-control input-lg',
        'placeholder':'Password'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs = {'class':'form-control input-lg',
        'placeholder':'Password confirmation'}))
    image_path = forms.CharField(required=False,widget=forms.HiddenInput())
    
    

    class Meta:
        model = User
        fields = ('email', 'username','full_name','image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class':'form-control input-lg','placeholder':'email'})
        self.fields['username'].widget.attrs.update({'class':'form-control input-lg','placeholder':'Login'})
        self.fields['full_name'].widget.attrs.update({'class':'form-control input-lg','placeholder':'Imię Nazwisko'})
        self.fields['image'].widget.attrs.update({'onchange':"document.getElementById('blah').src = window.URL.createObjectURL(this.files[0])","id":"inpFile",})
        
        
        #self.files['image'].temporary_file_path()
     

 
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    

    
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form,OTPAuthenticationFormMixin):
    query = forms.CharField(label='Username / Email',widget=forms.TextInput(attrs = {'class':'form-control input-lg',
        'placeholder':'Email/Login'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs = {'class':'form-control input-lg',
        'placeholder':'Password'}))
    otp_device = forms.CharField(required=False, widget=forms.Select)
    otp_token = forms.CharField(required=False, widget=forms.TextInput(attrs={'autocomplete': 'off','placeholder':'Token','class':'form-control input-lg'}))


    
    
    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')
        token  = self.cleaned_data.get('otp_token')
        user_qs_final = User.objects.filter(
                Q(username__iexact=query) |
                Q(email__iexact=query)
            ).distinct()
        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("Invalid credentials - user does note exist")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError("credentials are not correct")

        device = TOTPDevice.objects.filter(user=user_obj)
        print(device)
        if  device.exists():
            device = TOTPDevice.objects.get(user=user_obj)
            self.cleaned_data['otp_device'] = self.device_choices(user_obj)
            otp=self.cleaned_data.get('otp_device')

            self.clean_otp(user_obj)
        else:

            self.add_error('otp_device',"Device doesn't exist")
            

        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)


