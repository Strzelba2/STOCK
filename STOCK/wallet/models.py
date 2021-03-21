from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from WIG.models import CompanyData , Quotes_last , NCData,NC_Quotes_last

# Create your models here.
currency_choices= (
    ("USD", "USD"),
    ("EUR", "EUR"),
    ("GBP", "GBP"),
    ("PLN", "PLN")
    )
order = (
    ("Zakup","Zakup"),
    ("Sprzedarz","Sprzedarz")
)

class Currency_account(models.Model):
       
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE )
    name = models.CharField(max_length=30)
    currency = models.CharField(max_length=9,
                  choices = currency_choices,
                  default="PLN")
    cash = models.FloatField(blank=True, null=True)
    average_exchange =  models.FloatField(blank=True, null=True)
    

    def __str__(self):
        return  str(self.name)





class Broker_account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE )
    name = models.CharField(max_length=30)
    cash = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=9,
                  choices = currency_choices,
                  default="PLN")

    def __str__(self):
        return  str(self.name)

class Stocks(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE )
    stock = models.ForeignKey(CompanyData,on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker_account,on_delete=models.CASCADE)
    price_buy = models.FloatField()
    amount = models.IntegerField()
    currency = models.CharField(max_length=9,
                  choices = currency_choices,
                  default="PLN")
    last_price = models.ForeignKey(Quotes_last,on_delete=models.CASCADE ,default = Quotes_last.objects.all().last().id)

    def acquisition_cost(self):
        return  self.price_buy  *self.amount

    def worth(self):
        return self.last_price.Closing_price * self.amount

    def profit(self):
        
        return  self.worth() - self.acquisition_cost()
    def profit_pr (self):
        return (self.worth() - self.acquisition_cost())/self.acquisition_cost()*100

    def __str__(self):
        return  str(self.stock)

class NC(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE )
    stock = models.ForeignKey(NCData,on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker_account,on_delete=models.CASCADE)
    price_buy = models.FloatField()
    amount = models.IntegerField()
    currency = models.CharField(max_length=9,
                  choices = currency_choices,
                  default="PLN")
    last_price = models.ForeignKey(NC_Quotes_last,on_delete=models.CASCADE ,default = Quotes_last.objects.all().last().id)

    def acquisition_cost(self):
        return  self.price_buy  *self.amount

    def worth(self):
        return self.last_price.Closing_price * self.amount

    def profit(self):
        
        return  self.worth() - self.acquisition_cost()
    def profit_pr (self):
        return (self.worth() - self.acquisition_cost())/self.acquisition_cost()*100

    def __str__(self):
        return  str(self.stock)

class Stocks_transfer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE )
    stock = models.ForeignKey(CompanyData,on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker_account,on_delete=models.CASCADE)
    price = models.FloatField()
    ammount = models.IntegerField(default=1)
    order = models.CharField(max_length=9,
                  choices = order,
                  default="Zakup")
    cash_after_broker = models.FloatField(blank=True, null=True)
    day_transfer = models.DateField( auto_now=False, auto_now_add=False)

class NC_transfer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE )
    stock = models.ForeignKey(NCData,on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker_account,on_delete=models.CASCADE)
    price = models.FloatField()
    ammount = models.IntegerField(default=1)
    order = models.CharField(max_length=9,
                  choices = order,
                  default="Zakup")
    cash_after_broker = models.FloatField(blank=True, null=True)
    day_transfer = models.DateField( auto_now=False, auto_now_add=False)

class broker_transfer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE )
    account = models.ForeignKey("Currency_account",on_delete=models.CASCADE )
    account_broker = models.ForeignKey("Broker_account",on_delete=models.CASCADE )
    cash = models.FloatField(blank=True, null=True)
    title = models.TextField(max_length=400,blank=True, null=True)
    cash_after = models.FloatField(blank=True, null=True)
    cash_after_broker = models.FloatField(blank=True, null=True)
    day_transfer = models.DateField( auto_now=False, auto_now_add=False)

    def __str__(self):
        return   str(self.user)

class Bank_transfer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE )
    account = models.ForeignKey("Currency_account",on_delete=models.CASCADE )
    cash = models.FloatField(blank=True, null=True)
    title = models.TextField(max_length=400,blank=True, null=True)
    cash_after = models.FloatField(blank=True, null=True)
    day_transfer = models.DateField( auto_now=False, auto_now_add=False)

    def __str__(self):
        return   str(self.user)



class Cantor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE )
    day_transfer = models.DateField( auto_now=False, auto_now_add=False)
    currency_account_to = models.ForeignKey("Currency_account",related_name="currency_account_to", on_delete=models.CASCADE )
    currency_account_for = models.ForeignKey("Currency_account",related_name="currency_account_for",on_delete=models.CASCADE )
    cash_to = models.FloatField(blank=True, null=True)
    cash_for = models.FloatField(blank=True, null=True)
    exchange_rate = models.FloatField(blank=True, null=True)
    cash_after = models.FloatField(blank=True, null=True)
    cash_after_for = models.FloatField(blank=True, null=True)
    exchange_rate_after = models.FloatField(blank=True, null=True)

    def __str__(self):
        return  str(self.currency_account_to) + str(self.cash_to) + str(self.day_transfer)



