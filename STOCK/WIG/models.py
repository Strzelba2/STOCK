from __future__ import unicode_literals
from django.db import models
import datetime


# Create your models here.




class CompanyData(models.Model):
    Symbol = models.CharField( max_length=100)
    Name_company = models.CharField( max_length=100)


    def __str__(self):
        return  self.Name_company 


class Quotes (models.Model):
    Name_company = models.ForeignKey("CompanyData",on_delete=models.CASCADE)
    Day_trading = models.DateField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField()
    Volume = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return  self.Name_company.Name_company + " z dnia:       " + str(self.Day_trading)

class Quotes_last (models.Model):
    Name_company = models.ForeignKey("CompanyData",on_delete=models.CASCADE)
    Day_trading = models.DateTimeField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField(blank=True, null=True)
    Volume = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return  self.Name_company.Name_company + " z dnia:       " + str(self.Day_trading)

class IndexData(models.Model):
    Symbol = models.CharField( max_length=100)
    Name_Index = models.CharField( max_length=100)


    def __str__(self):
        return "INdex "+ self.Name_Index 


class Index (models.Model):
    Name_Index = models.ForeignKey("IndexData",on_delete=models.CASCADE)
    Day_trading = models.DateField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField()
    Volume = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return  self.Name_Index.Name_Index + " z dnia:       " + str(self.Day_trading)

class Index_Last (models.Model):
    Name_Index = models.ForeignKey("IndexData",on_delete=models.CASCADE)
    Day_trading = models.DateTimeField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField()


    def __str__(self):
        return  self.Name_Index.Name_Index + " z dnia:       " + str(self.Day_trading)


class WaresData(models.Model):
    Symbol = models.CharField( max_length=100)
    Name_ware = models.CharField( max_length=100)


    def __str__(self):
        return "Ware : "+ self.Name_ware 


class Wares (models.Model):
    Name_ware = models.ForeignKey("WaresData",on_delete=models.CASCADE)
    Day_trading = models.DateField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField()
    Volume = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return  self.Name_ware.Name_ware + " z dnia:       " + str(self.Day_trading)

class Wares_Last (models.Model):
    Name_ware = models.ForeignKey("WaresData",on_delete=models.CASCADE)
    Day_trading = models.DateTimeField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField()


    def __str__(self):
        return  self.Name_ware.Name_ware + " z dnia:       " + str(self.Day_trading)

class CurrencyData(models.Model):
    Symbol = models.CharField( max_length=100)
    Name_Currency = models.CharField( max_length=100)


    def __str__(self):
        return "Ware : "+ self.Name_Currency 


class Currency (models.Model):
    Name_Currency = models.ForeignKey("CurrencyData",on_delete=models.CASCADE)
    Day_trading = models.DateField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField()


    def __str__(self):
        return  self.Name_Currency.Name_Currency + " z dnia:       " + str(self.Day_trading)

class Currency_Last (models.Model):
    Name_Currency = models.ForeignKey("CurrencyData",on_delete=models.CASCADE)
    Day_trading = models.DateTimeField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField()


    def __str__(self):
        return  self.Name_Currency.Name_Currency + " z dnia:       " + str(self.Day_trading)
