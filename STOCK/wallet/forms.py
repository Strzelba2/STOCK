from django import forms 
from .models import  Currency_account,Bank_transfer,Cantor,NC_transfer
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

def get_question_form(conditional_model):
    class NC_transfer_form(forms.ModelForm):
        class Meta:
    
            model = conditional_model
            fields = ["order","price","ammount","day_transfer"]

        def __init__(self,broker_id,stock, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.broker_id = broker_id
            self.stock = stock.first()
            
            if not self.stock:

                self.fields['order'].choices=[('Zakup','Zakup')]

            self.fields['day_transfer'].widget.attrs.update({'autocomplete': 'off'})

        def clean(self,**kwargs):

            cleaned_data = super().clean()
            order = cleaned_data.get('order')
            ammount =cleaned_data.get('ammount')

            price =cleaned_data.get('price')

            if ammount == 0:
                msg = "Ilość musi być większa niż 0"
                self.add_error('ammount', msg)
            if price == 0:
                msg = "Cena musi być większa niż 0"
                self.add_error('price', msg)

            if order == "Zakup":
                if self.broker_id.cash < ammount*price:

                    raise ValidationError(
                        "Za mało środków na koncie"

                    )

            if  self.stock:
                if order == "Sprzedarz":
                    
                    if ammount > self.stock.amount:
                        raise ValidationError(
                            mark_safe("Za mało akcji na koncie.<br/>Zmniejsz ilość akcji na sprzedarz")
                        )

    return NC_transfer_form
        










