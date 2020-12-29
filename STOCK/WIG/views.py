from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView 
from .models import CompanyData , Quotes ,IndexData , Index,Quotes_last
from .WIG_scrap import SCRAP
from .WIG_udate import UPDATE_SCRAP
from pathlib import Path
from .Random_proxy import Random
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
        driver = Random().get_Driver()
        #SCRAP.down_index(driver)
        #SCRAP.down_wares(driver)
        #SCRAP.down_currency(driver)
        SCRAP.down_company_quote(driver)
        driver.quit()

        my_lis["quote_init"] = True

        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(my_lis))
            outfile.close()

    path = Path(__file__).parent
    filename = os.path.join(path,'init_data.json')
    with open(filename) as file:
        my_lis=json.load(file)

    financial_data = my_lis.get("financial_data")

    if financial_data is False:
        print("if")
        #SCRAP.down_company_financial()

        my_lis["financial_data"] = True

        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(my_lis))
            outfile.close()

    return redirect('home')

def update_data(request):

    driver = Random().get_Driver()

    UPDATE_SCRAP.update_Company(driver)
    UPDATE_SCRAP.update_Currency(driver)
    UPDATE_SCRAP.update_Index(driver)
    UPDATE_SCRAP.update_Wares(driver)
    driver.quit()
 


    return HttpResponse(status=200)


class Home (ListView):

    model = CompanyData
    template_name = "WIG/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Index_obj = Quotes_last.objects.all()
        context["list"] = Index_obj

        return context

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

class Analysis (ListView): 
    model = Quotes
    fields = []
    template_name = "WIG/analiza.html"
    context_object_name = "data"
 
   
    
    def get_queryset(self):
        print("działa")
 
        name = self.request.GET.get('name')
        print(name)
        Company = CompanyData.objects.get(Symbol = name)
        print(Company)
        
        Quotes_company =list(Quotes.objects.filter(Name_company = Company))
        data = serializers.serialize('json', Quotes_company)
        
        return data



