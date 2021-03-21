from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView 
from .models import CompanyData , Quotes ,IndexData , Index,Quotes_last,Index_Last,Wares_Last,Currency_Last,Currency,CurrencyData,WaresData,Wares,NC_Quotes_last,NCData,NC_Quotes
from .WIG_scrap import SCRAP
from .WIG_udate import UPDATE_SCRAP
from pathlib import Path
import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers


# Create your views here.

def init_data(request):
    path = Path(__file__).parent
    filename = os.path.join(path,'init_data.json')

    with open(filename) as file:
        my_lis=json.load(file)

    data_init = my_lis.get("quote_init")

    if data_init is False:

        #SCRAP().down_index()
        #SCRAP().down_wares()
        #SCRAP().down_currency()
        #SCRAP().down_company_quote()
        #SCRAP().down_NC_quote()

        SCRAP.down_RSI()

        my_lis["quote_init"] = True

        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(my_lis))
            outfile.close()
    ''' 
    path = Path(__file__).parent
    filename = os.path.join(path,'init_data.json')
    with open(filename) as file:
        my_lis=json.load(file)

    financial_data = my_lis.get("financial_data")

    if financial_data is False:

        #SCRAP.down_company_financial()

        my_lis["financial_data"] = True

        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(my_lis))
            outfile.close()
    '''


    return redirect('home')

def update_WIG(request):
    
    UPDATE_SCRAP.update_Company()

    return redirect('home')

def update_NC(request):
    
    UPDATE_SCRAP.update_NC()

    return redirect('home')

def update_Index(request):

    UPDATE_SCRAP.update_Index()

    return redirect('home')
    
def update_Wares(request):

    UPDATE_SCRAP.update_Wares()

    return redirect('home')

def update_Currency(request):

    UPDATE_SCRAP.update_Currency()

    return redirect('home')


class Home (ListView):

    model = CompanyData
    template_name = "WIG/home.html"
    context_object_name = "quates_data"
    ordering = ['Name',]

    def __init__(self, **kwargs):
        self.list_order = {'Name':'-Name','Day_trading':'-Day_trading','Closing_price':'-Closing_price','Change_price':'-Change_price'
                ,'Opening_price':'-Opening_price','Highest_price':'-Highest_price','Lowest_price':'-Lowest_price','Volume':'-Volume'
                ,'RSI':'-RSI','Stochastic':'-Stochastic'}
        self.tabela_nav = {"Nazwa":["Name","fa fa-angle-up"],"Data":['Day_trading',"fa fa-angle-up"],"Kurs":['Closing_price',"fa fa-angle-up"]
                ,"Zmiana":["Change_price","fa fa-angle-up"],"Cena otwarcia":['Opening_price',"fa fa-angle-up"]
                ,"Cena Max.":['Highest_price',"fa fa-angle-up"],"Cena Min.":['Lowest_price',"fa fa-angle-up"],"Wolumen":["Volume","fa fa-angle-up"]
                ,"RSI":["RSI","fa fa-angle-up"]
                }

    def get(self, request, *args, **kwargs):
        
        quates = request.GET.get("quates")

        return super().get(request, *args, **kwargs)

    def get_queryset(self):

        ordering = self.get_ordering()
        quates = self.request.GET.get("quotes")


        if quates == None or quates == "":

            data = Quotes_last.objects.all().order_by(ordering)
   
        else:

            if quates == "WIG":
                data = Quotes_last.objects.all().order_by(ordering)

            elif quates == "Waluty":
                data = Currency_Last.objects.all().order_by(ordering)

            elif quates == "Index":
                data = Index_Last.objects.all().order_by(ordering)

            elif quates == "Towary":
                data = Wares_Last.objects.all().order_by(ordering)
            elif quates == "NC":
                data = NC_Quotes_last.objects.all().order_by(ordering)

        return data

    def get_ordering(self):  

        self.ordering = self.request.GET.get("orderlist")

        if self.ordering == None: 
 
            self.ordering = next(iter(self.list_order)) 
  
        else:
            if self.ordering in self.list_order:

                self.ordering = self.list_order.get(self.ordering,'')

            else:
                self.ordering=list(self.list_order.keys())[list(self.list_order.values()).index(self.ordering)]

        return  self.ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quates = self.request.GET.get("quotes")


        if self.ordering in self.list_order:
            fafa = "fa fa-angle-down"
            i = list(self.list_order.keys()).index(self.ordering)
            self.tabela_nav[list(self.tabela_nav)[i]][0] = self.ordering
            self.tabela_nav[list(self.tabela_nav)[i]][1] = fafa
        else:

            fafa = "fa fa-angle-up"
            i = list(self.list_order.values())
            self.tabela_nav[list(self.tabela_nav)[i.index(self.ordering)]][0] = self.ordering
            self.tabela_nav[list(self.tabela_nav)[i.index(self.ordering)]][1] = fafa
        
        if quates == None or quates == "":

            class_choose= ["divQuotes","divQuotes","divQuotes","divQuotes","divQuotes"]
    
            context["genre"] = "WIG"
            context["choose"] = class_choose

        else:

            if quates == "WIG":
                class_choose= ["divQuotes active","divQuotes","divQuotes","divQuotes","divQuotes"]

                context["choose"] = class_choose
                context["genre"] = quates

            elif quates == "NC":
                class_choose= ["divQuotes","divQuotes active","divQuotes","divQuotes","divQuotes"]
                 
                context["choose"] = class_choose
                context["genre"] = quates

            elif quates == "Waluty":
                class_choose= ["divQuotes","divQuotes","divQuotes active","divQuotes","divQuotes"]
                 
                context["choose"] = class_choose
                context["genre"] = quates

            elif quates == "Index":
                class_choose= ["divQuotes","divQuotes","divQuotes","divQuotes active","divQuotes"]

                context["choose"] = class_choose
                context["genre"] = quates

            elif quates == "Towary":
                class_choose= ["divQuotes","divQuotes","divQuotes","divQuotes","divQuotes active"]

                context["choose"] = class_choose
                context["genre"] = quates

        context["tabela_nav"] = self.tabela_nav

        return context



        
        
'''
class Chart_data(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAdminUser]

    def get(self, request,name, format=None):
        print("działa")

        print(name)
        Company = CompanyData.objects.get(Symbol = name)
        print(Company)
        
        """
        Return a list of all users.
        """
        Quotes_company = list(Quotes.objects.filter(Name_company = Company))
        data = serializers.serialize('json', Quotes_company)
        print(data)
        return Response(data)
'''

class Analysis (ListView): 
    model = Quotes
    fields = []
    template_name = "WIG/analiza.html"
    context_object_name = "data"
    ordering = 'Day_trading'
 
   
    
    def get_queryset(self):
        ordering = self.get_ordering()
 
        name = self.request.GET.get('name')
        genre = self.request.GET.get('genre')

        if genre == "WIG":

            Company = CompanyData.objects.get(Name = name)
            Quotes_company =list(Quotes.objects.filter(Name = Company).order_by(ordering))
            data = serializers.serialize('json', Quotes_company)
        if genre == "NC":
            Company = NCData.objects.get(Name = name)
            Quotes_company =list(NC_Quotes.objects.filter(Name = Company).order_by(ordering))
            data = serializers.serialize('json', Quotes_company)
        elif genre == "Waluty":

            Currency_data = CurrencyData.objects.get(Name = name)
            Currency_company =list(Currency.objects.filter(Name = Currency_data).order_by(ordering))
            data = serializers.serialize('json', Currency_company)
        elif genre == "Index":

            Index_data = IndexData.objects.get(Name = name)
            Index_company =list(Index.objects.filter(Name = Index_data).order_by(ordering))
            data = serializers.serialize('json', Index_company)
        elif genre == "Towary":

            Wares_data = WaresData.objects.get(Name = name)
            Wares_company =list(Wares.objects.filter(Name = Wares_data).order_by(ordering))
            data = serializers.serialize('json', Wares_company)
        
        return data



