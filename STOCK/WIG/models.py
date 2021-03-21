from __future__ import unicode_literals
from django.db import models
import datetime


# Create your models here.


class NCData(models.Model):
    Symbol = models.CharField( max_length=100)
    Name = models.CharField( max_length=100)


    def __str__(self):
        return  self.Name

class NC_Quotes (models.Model):
    Name = models.ForeignKey("NCData",on_delete=models.CASCADE)
    Day_trading = models.DateField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField()
    Volume = models.BigIntegerField(blank=True, null=True)
    RSI = models.FloatField(blank=True, null=True)
    av_gain = models.FloatField(blank=True, null=True)
    av_loss = models.FloatField(blank=True, null=True)
    Stochastic = models.FloatField(blank=True, null=True)

    def __str__(self):
        return  self.Name.Name + " z dnia:       " + str(self.Day_trading)

class NC_Quotes_last (models.Model):
    Name = models.ForeignKey("NCData",on_delete=models.CASCADE)
    Day_trading = models.DateTimeField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField(blank=True, null=True)
    Volume = models.BigIntegerField(blank=True, null=True)
    Change_price = models.FloatField(blank=True, null=True)
    RSI = models.FloatField(blank=True, null=True)
    Stochastic = models.FloatField(blank=True, null=True)

    def __str__(self):
        return  self.Name.Name + " z dnia:       " + str(self.Day_trading)

class CompanyData(models.Model):
    Symbol = models.CharField( max_length=100)
    Name = models.CharField( max_length=100)


    def __str__(self):
        return  self.Name


class Quotes (models.Model):
    Name = models.ForeignKey("CompanyData",on_delete=models.CASCADE)
    Day_trading = models.DateField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField()
    Volume = models.BigIntegerField(blank=True, null=True)
    RSI = models.FloatField(blank=True, null=True)
    av_gain = models.FloatField(blank=True, null=True)
    av_loss = models.FloatField(blank=True, null=True)
    Stochastic = models.FloatField(blank=True, null=True)

    def __str__(self):
        return  self.Name.Name + " z dnia:       " + str(self.Day_trading)

class Quotes_last (models.Model):
    Name = models.ForeignKey("CompanyData",on_delete=models.CASCADE)
    Day_trading = models.DateTimeField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField(blank=True, null=True)
    Volume = models.BigIntegerField(blank=True, null=True)
    Change_price = models.FloatField(blank=True, null=True)
    RSI = models.FloatField(blank=True, null=True)
    Stochastic = models.FloatField(blank=True, null=True)

    def __str__(self):
        return  self.Name.Name + " z dnia:       " + str(self.Day_trading)

    


class IndexData(models.Model):
    Symbol = models.CharField( max_length=100)
    Name = models.CharField( max_length=100)


    def __str__(self):
        return  self.Name


class Index (models.Model):
    Name = models.ForeignKey("IndexData",on_delete=models.CASCADE)
    Day_trading = models.DateField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField()
    Volume = models.BigIntegerField(blank=True, null=True)
    RSI = models.FloatField(blank=True, null=True)
    av_gain = models.FloatField(blank=True, null=True)
    av_loss = models.FloatField(blank=True, null=True)
    Stochastic = models.FloatField(blank=True, null=True)

    def __str__(self):
        return  self.Name.Name + " z dnia:       " + str(self.Day_trading)

class Index_Last (models.Model):
    Name = models.ForeignKey("IndexData",on_delete=models.CASCADE)
    Day_trading = models.DateTimeField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField()
    Change_price = models.FloatField(blank=True, null=True)
    RSI = models.FloatField(blank=True, null=True)
    Stochastic = models.FloatField(blank=True, null=True)


    def __str__(self):
        return  self.Name.Name + " z dnia:       " + str(self.Day_trading)




class WaresData(models.Model):
    Symbol = models.CharField( max_length=100)
    Name = models.CharField( max_length=100)


    def __str__(self):
        return  self.Name


class Wares (models.Model):
    Name = models.ForeignKey("WaresData",on_delete=models.CASCADE)
    Day_trading = models.DateField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField()
    Volume = models.BigIntegerField(blank=True, null=True)
    RSI = models.FloatField(blank=True, null=True)
    av_gain = models.FloatField(blank=True, null=True)
    av_loss = models.FloatField(blank=True, null=True)
    Stochastic = models.FloatField(blank=True, null=True)

    def __str__(self):
        return  self.Name.Name + " z dnia:       " + str(self.Day_trading)

class Wares_Last (models.Model):
    Name = models.ForeignKey("WaresData",on_delete=models.CASCADE)
    Day_trading = models.DateTimeField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField()
    Change_price = models.FloatField(blank=True, null=True)
    RSI = models.FloatField(blank=True, null=True)
    Stochastic = models.FloatField(blank=True, null=True)


    def __str__(self):
        return  self.Name.Name + " z dnia:       " + str(self.Day_trading)

class CurrencyData(models.Model):
    Symbol = models.CharField( max_length=100)
    Name = models.CharField( max_length=100)


    def __str__(self):
        return self.Name


class Currency (models.Model):
    Name = models.ForeignKey("CurrencyData",on_delete=models.CASCADE)
    Day_trading = models.DateField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField(blank=True, null=True)
    RSI = models.FloatField(blank=True, null=True)
    av_gain = models.FloatField(blank=True, null=True)
    av_loss = models.FloatField(blank=True, null=True)
    Stochastic = models.FloatField(blank=True, null=True)


    def __str__(self):
        return  self.Name.Name + " z dnia:       " + str(self.Day_trading)

class Currency_Last (models.Model):
    Name = models.ForeignKey("CurrencyData",on_delete=models.CASCADE)
    Day_trading = models.DateTimeField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField()
    Change_price = models.FloatField(blank=True, null=True)
    RSI = models.FloatField(blank=True, null=True)
    Stochastic = models.FloatField(blank=True, null=True)


    def __str__(self):
        return  self.Name.Name + " z dnia:       " + str(self.Day_trading)
