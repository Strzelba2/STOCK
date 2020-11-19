from __future__ import unicode_literals
from django.db import models

# Create your models here.

class CompanyData(models.Model):
    Name_company = models.CharField( max_length=100)
    Link_to_Search = models.CharField( max_length=100)


class Quotes (models.Model):
    Name_company = models.ForeignKey("CompanyData",on_delete=models.CASCADE)
    Day_trading = models.DateField( auto_now=False, auto_now_add=False)
    Opening_price = models.FloatField()
    Highest_price = models.FloatField()
    Lowest_price = models.FloatField()
    Closing_price = models.FloatField()
    Volume = models.IntegerField()
