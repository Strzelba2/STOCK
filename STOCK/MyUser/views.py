from django.shortcuts import render, redirect,reverse
from django.contrib.auth import login, get_user_model, logout
from random import randint
from django.conf import settings
from django.core.mail import EmailMessage, send_mail,EmailMultiAlternatives
from .models import MyUsers
from django.db.models import Q
from django.contrib.auth import get_user_model
import time
from django.utils import timezone
from . import facebook
from . import google
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect,HttpResponse
import random
from django.template import loader
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.edit import CreateView 
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
from django.core.exceptions import ValidationError
import datetime
from django.views.decorators.cache import never_cache
from django.core.exceptions import PermissionDenied
from datetime import timedelta

from .forms import UserCreationForm, UserLoginForm , RegisterNumForm
from .tokens import account_activation_token

User =  get_user_model ()

from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.models import Device
from django_otp import devices_for_user
import io
import base64


class Register(CreateView):
    model = MyUsers
    form_class = UserCreationForm
    template_name = "auth/register.html"
    html_email_template_name = "auth/email_confirmation.html"
    email_template_name = "auth/email_confimation.txt"
    subject_template_name = "auth/email_confimation.txt"

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        html_body = loader.render_to_string(html_email_template_name, context)
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        email_message.attach_alternative(html_body, "text/html")

        email_message.send()


    def get_success_url(self):
        return reverse("login_view")
    def form_valid(self, form):
        form.save()
        username=form['username'].value()
        user=MyUsers.objects.get(username=username)
        from_email = settings.EMAIL_HOST_USER
        emails = form['email'].value()
        current_site = get_current_site(self.request)
        site_name = current_site.name
        domain = current_site.domain
        use_https = self.request.is_secure()
        subject_template_name = self.subject_template_name
        email_template_name = self.email_template_name
        html_email_template_name = self.html_email_template_name
        context = {
                'email': emails,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
        self.send_mail(
            subject_template_name, email_template_name, context, from_email,
            emails,html_email_template_name,
        )
        return super().form_valid(form)



class LoginConfirm( View):


    def get(self, request, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs
        self.user = self.get_user(kwargs['uidb64'])
        token = kwargs['token']
        
        for users in MyUsers.objects.all():
            date_valide = datetime.date.today() - users.date_joined.date()
            if date_valide.days > 2 and users.is_active is False:
                users.delete()
        if self.user is not None and account_activation_token.check_token(self.user, token):
            user=MyUsers.objects.get(username=self.user)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('wallet')
        elif self.user is not None and account_activation_token.check_token(self.user, token) is False :
            user=MyUsers.objects.get(username=self.user)
            if user.is_active is False:
                user.delete()
            form = UserCreationForm(request.POST or None)
            errorvalid="Link jest nie aktywny proszę ponownie się zarejestrować"
            return render(request, "auth/register.html", {'form':form,"errorvalid":errorvalid})

        else:
            # invalid link
            form = UserCreationForm(request.POST or None)
            errorvalid="Link jest nie aktywny proszę ponownie się zarejestrować"
            return render(request, "auth/register.html", {'form':form,"errorvalid":errorvalid})

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = MyUsers._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user



def get_user_totp_device( user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            
            return device

def login_view(request, *args, **kwargs):

    form = UserLoginForm(request.POST or None )


    if request.POST:
        if form.is_valid():
            print("if")
            user_obj = form.cleaned_data.get('user_obj')
            login(request, user_obj)
            user = request.user
            return redirect('wallet')
        else:
            if 'otp_device' in form.errors:

                user = request.user
                user_gr = MyUsers.objects.get(username = user)
                device = get_user_totp_device( user)
                if not device:
                    device = TOTPDevice(user=user_gr,name=user.username)
                    device.save()
                return HttpResponseRedirect(reverse('qrcode', kwargs={'pk': device.pk}))

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/login")



def facebook_view(request):
    token = request.POST.get('token')
    user_data = facebook.Facebook.validate(token)

    try:
        facebook_user_id = user_data['id']
        email = user_data['email']
        username = user_data['name']
        facebook_picture = user_data['picture']

        user = MyUsers.objects.filter(facebook_user_id = facebook_user_id)
        if not user.exists() and user.count != 1:
            username = "".join(username.split(' ')).lower()
            if  MyUsers.objects.filter(username=username).exists():
                username = username + str(random.randint(0, 1000))
            if MyUsers.objects.filter(email=email).exists():
                user = MyUsers.objects.get(email= email)
                user.facebook_user_id = facebook_user_id
                user.facebook_picture = facebook_picture 
                user.save()
            else:
                user = MyUsers(username=username)
                user.is_staff = True
                user.is_superuser = False
                user.email = email
                user.is_active = True
                user.facebook_user_id = facebook_user_id
                user.facebook_picture = facebook_picture 
                user.save()
        user = MyUsers.objects.get(facebook_user_id = facebook_user_id)
        login(request, user)
        

    except:
        return JsonResponse({'success':False, 'error':user_data}, status=400)
    url='/wallet/'
    return JsonResponse({'success':True, 'url':url}, status=200)


def Google_view(request):
    auth_token = request.POST.get('token')
    user_data = google.Google.validate(auth_token)

    try:

        google_user_id = user_data['sub']
        email = user_data['email']
        google_picture = user_data['picture']
        username = user_data['name']
        user = MyUsers.objects.filter(google_user_id = google_user_id)
        if not user.exists() and user.count != 1:
            username = "".join(username.split(' ')).lower()
            if  MyUsers.objects.filter(username=username).exists():
                username = username + str(random.randint(0, 1000))
            if MyUsers.objects.filter(email=email).exists():
                user = MyUsers.objects.get(email= email)
                user.google_user_id = google_user_id
                user.google_picture = google_picture 
                user.save()
            else:
                user = MyUsers(username=username)
                user.is_staff = True
                user.is_superuser = False
                user.email = email
                user.is_active = True
                user.google_user_id = google_user_id
                user.google_picture = google_picture 
                user.save()
        user = MyUsers.objects.get(google_user_id = google_user_id)
        login(request, user)
        


    except:
        return JsonResponse({'success':False, 'error':user_data}, status=400)
    url='/wallet/'
    
    return JsonResponse({'success':True, 'url':url}, status=200)


def qrcode_view( request, pk):

        device = TOTPDevice.objects.get(pk=pk)

        print("działą")

        import qrcode
        import qrcode.image.svg
        stream = io.BytesIO()
        img = qrcode.make(device.config_url, image_factory=qrcode.image.svg.SvgImage)
        img.save(stream)
        img_str = base64.b64encode(stream.getvalue()).decode()
        return render(request,"auth/qrcode.html",{'image':img_str})
            
            
            
            



