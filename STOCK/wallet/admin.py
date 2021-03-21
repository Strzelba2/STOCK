from django.contrib import admin
from .models import Cantor , Bank_transfer, Currency_account,Stocks,Broker_account,Stocks_transfer,broker_transfer,NC,NC_transfer

# Register your models here.

admin.site.register(Cantor)
admin.site.register(Bank_transfer)
admin.site.register(Broker_account)
admin.site.register(Stocks)
admin.site.register(Stocks_transfer)
admin.site.register(broker_transfer)
admin.site.register(NC)
admin.site.register(NC_transfer)

