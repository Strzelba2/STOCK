from django.contrib import admin
from .models import CompanyData , Quotes,Index,IndexData,Wares,WaresData,Currency,CurrencyData,Quotes_last,Currency_Last,Index_Last,Wares_Last
# Register your models here.


admin.site.register(CompanyData)
admin.site.register(Quotes)
admin.site.register(Index)
admin.site.register(IndexData)
admin.site.register(Wares)
admin.site.register(WaresData)
admin.site.register(Currency)
admin.site.register(CurrencyData)
admin.site.register(Quotes_last)
admin.site.register(Index_Last)
admin.site.register(Wares_Last)
admin.site.register(Currency_Last)


