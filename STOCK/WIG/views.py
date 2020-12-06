from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView 
from .models import CompanyData , Quotes ,IndexData , Index
from .WIG_scrap import SCRAP
from .WIG_udate import UPDATE_SCRAP
from pathlib import Path
import os
import json

# Create your views here.

def init_data(request):
    path = Path(__file__).parent
    filename = os.path.join(path,'init_data.json')

    with open(filename) as file:
        my_lis=json.load(file)

    data_init = my_lis.get("quote_init")

    if data_init is False:
        SCRAP.down_index()
        SCRAP.down_wares()
        SCRAP.down_currency()
        SCRAP.down_company_quote()

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
        SCRAP.down_company_financial()

        my_lis["financial_data"] = True

        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(my_lis))
            outfile.close()

    return redirect('home')

def update_data(request):

    print("działa")


    UPDATE_SCRAP.update_Company()
    UPDATE_SCRAP.update_Currency()
    UPDATE_SCRAP.update_Index()
    UPDATE_SCRAP.update_Wares()

    return HttpResponse(status=200)


class Home (ListView):

    model = CompanyData
    template_name = "WIG/home.html"

    def get_queryset(self):
        Index_obj = IndexData.objects.get(pk=1)
        data = Index.objects.filter(Name_Index=Index_obj)
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Index_obj = IndexData.objects.get(pk=1)
        context["list"] = list(Index.objects.filter(Name_Index=Index_obj))

        return context



