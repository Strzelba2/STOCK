
from django.views.generic.base import TemplateView
from django.shortcuts import redirect ,reverse
from django.views.generic import  ListView ,  CreateView
from django.views.generic.edit import  DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Currency_account,Bank_transfer,Cantor,Broker_account,Stocks,Stocks_transfer,NC_transfer,NC
from django.shortcuts import render
from django.http.response import JsonResponse
from itertools import chain
from WIG.models import Currency_Last,CurrencyData,Quotes_last,CompanyData,NCData,NC_Quotes_last
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Q,CharField,Value
from django.core import serializers
from rest_framework.response import Response
from .forms import  get_question_form






# Create your views here.


class wallet(LoginRequiredMixin,TemplateView):
    template_name = 'wallet/wallet.html'

    def cash_average(self,obj):
        cash_dict = {"cash":0,"average":0}
        for x in obj:
            cash = cash_dict["cash"]
            average = cash_dict["average"]  
            if x.cash == 0:
                continue
            else:
                cash_dict["cash"]   = cash + x.cash

                average_all = (cash*average+x.cash*x.average_exchange)/cash_dict["cash"]
                cash_dict["average"] =round(average_all,2)
        return cash_dict


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cashPLN = 0

        account_PLN= Currency_account.objects.filter(user = self.request.user,currency = "PLN")
        account_USD= Currency_account.objects.filter(user = self.request.user,currency = "USD")
        account_EUR= Currency_account.objects.filter(user = self.request.user,currency = "EUR")
        account_GBP= Currency_account.objects.filter(user = self.request.user,currency = "GBP")

        for x in account_PLN:
            cashPLN += x.cash

        cashUSD = self.cash_average(account_USD)
        cashEUR = self.cash_average(account_EUR)
        cashGBP = self.cash_average(account_GBP)

        account_broker= Broker_account.objects.filter(user = self.request.user)



        context["account_PLN"] = account_PLN
        context["account_USD"] = account_USD
        context["account_EUR"] = account_EUR
        context["account_GBP"] = account_GBP

        context["account_broker"] = account_broker

        context["cashPLN"] = cashPLN
        context["cashUSD"] = cashUSD
        context["cashEUR"] = cashEUR
        context["cashGBP"] = cashGBP

        return context
        

class Cash_Deposit (LoginRequiredMixin,CreateView):  
    template_name = 'wallet/cashdeposit.html'
    model = Bank_transfer
    fields = ["cash","day_transfer","title"]


    def get_success_url(self):
 
        return reverse("wallet")

    def get_form(self):

        form = super(Cash_Deposit, self).get_form()
        account_name = self.request.GET.get("account_name")
        if account_name:
            self.request.session['account_name'] = account_name

        form.fields['cash'].widget.attrs.update({'placeholder':'PLN'})
        form.fields['day_transfer'].widget.attrs.update({'autocomplete': 'off'})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["account"] = self.request.session['account_name']
        context["title_account"] = "Wpłata"
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        transfer_account = Currency_account.objects.get(user = self.request.user,name = self.request.session['account_name'])
        form.instance.account = transfer_account
       
        sum_cash = form.cleaned_data['cash'] + transfer_account.cash
        form.instance.cash_after = sum_cash

        transfer_account.cash = sum_cash
        transfer_account.save()

        return super().form_valid(form)


class Cash_withdrawal (LoginRequiredMixin,CreateView):  
    template_name = 'wallet/cashdeposit.html'
    model = Bank_transfer
    fields = ["cash","day_transfer","title"]


    def get_success_url(self):
 
        return reverse("wallet")

    def get_form(self):

        form = super(Cash_withdrawal, self).get_form()
        account_name = self.request.GET.get("account_name")
        if account_name:
            self.request.session['account_name'] = account_name

        form.fields['cash'].widget.attrs.update({'placeholder':'PLN'})
        form.fields['day_transfer'].widget.attrs.update({'autocomplete': 'off'})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["account"] = self.request.session['account_name']
        context["title_account"] = "Wypłata"
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        transfer_account = Currency_account.objects.get(user = self.request.user,name = self.request.session['account_name'])
        form.instance.account = transfer_account
       
        sum_cash =  transfer_account.cash -  form.cleaned_data['cash']
        form.instance.cash_after = sum_cash
        form.instance.cash = -form.cleaned_data['cash']

        transfer_account.cash = sum_cash
        transfer_account.save()

        return super().form_valid(form)

class Lista_Bank_transfer(LoginRequiredMixin,ListView):
    template_name = 'wallet/History_date.html'
    model = Bank_transfer
    context_object_name = "listaBankTransfer"
    fields = "__all__"

    def get_queryset(self,**kwargs):

        account = self.request.GET.get("account_name")
        exchange = self.request.GET.get("exchange")
        if exchange:
            self.request.session['exchange'] = exchange

        if account:
            self.request.session['account_name'] = account

        account_data = Currency_account.objects.get(name = self.request.session['account_name'])
        date_since = self.request.GET.get("date-since")
        date_to = self.request.GET.get("date-to")
        if date_since and date_to:
            
            if self.request.session['exchange'] == "exchange":
                data = Cantor.objects.filter(currency_account_to=account_data,day_transfer__range=(date_since,date_to)).order_by('-day_transfer')
            else:
                data1 = Bank_transfer.objects.filter(account=account_data  ,day_transfer__range=(date_since,date_to)).order_by('-day_transfer')
                data2 = Cantor.objects.filter(currency_account_for=account_data,day_transfer__range=(date_since,date_to)).order_by('-day_transfer')
                data = sorted(chain(data1, data2),key=lambda data: data.day_transfer, reverse=True)

            return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.session['exchange'] == "exchange":

            context["exchange"] = self.request.session['exchange']

        return context

class Lista_Stocks(LoginRequiredMixin,ListView):
    template_name = 'wallet/Stocks.html'
    model = Stocks
    context_object_name = "Stocks"
    fields = "__all__"

    def get_queryset(self, **kwargs):

        pk = self.kwargs['pk']

        self.broker_id = Broker_account.objects.get(id = pk)

        self.data = Stocks.objects.filter(broker = self.broker_id)
  
        return self.data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sum_acquisition_cost = 0
        sum_worth = 0
        for item in self.data:
            sum_acquisition_cost += item.acquisition_cost()
            sum_worth += item.worth()
        sum_profit = sum_worth - sum_acquisition_cost
        sum_profit_pr =  (sum_worth - sum_acquisition_cost)/sum_acquisition_cost*100
        context["sum_acquisition_cost"] = sum_acquisition_cost
        context["sum_worth"] = sum_worth
        context["sum_profit"] = sum_profit
        context["sum_profit_pr"] = sum_profit_pr
        context["sum_wallet"] = sum_profit + self.broker_id.cash
        context["cash"] = self.broker_id
        return context

class buy_stocks(LoginRequiredMixin,CreateView):
    template_name = 'wallet/buy_stocks.html'

    def get_success_url(self,**kwargs):
 
        return reverse("Lista_Stocks",kwargs={"pk":self.kwargs['pk']})
    
    def get_form_class(self,**kwargs):      
        self.broker_id = Broker_account.objects.get(id = self.kwargs['pk'])
        self.genre = self.kwargs['genre']

        if self.genre == "WIG":
            model = Stocks_transfer
            self.NC_stock = CompanyData.objects.get(Name=self.kwargs['stock'])
            self.amount = Stocks.objects.filter(broker=self.broker_id.id,stock=self.NC_stock)
        else:
            model = NC_transfer
            self.NC_stock = NCData.objects.get(Name=self.kwargs['stock'])
            self.amount = NC.objects.filter(broker=self.broker_id.id,stock=self.NC_stock)

        return get_question_form(model)

    def get_form_kwargs(self,**kwargs):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        

        kwargs = super(buy_stocks, self).get_form_kwargs()
        kwargs['broker_id'] = self.broker_id
        kwargs['stock'] = self.amount
        
        return kwargs

    def form_valid(self, form):
        price = form.cleaned_data['price']
        amount = form.cleaned_data['ammount']
        transaction = form.cleaned_data['order']
        form.instance.user = self.request.user
        form.instance.stock = self.NC_stock
        form.instance.broker = self.broker_id
        if transaction == "Zakup":
            form.instance.cash_after_broker = self.broker_id.cash -(price*amount)
        else:
            form.instance.cash_after_broker = self.broker_id.cash +(price*amount)

        if self.amount:
            NC_obj = self.amount.first()
            NCprice = NC_obj.price_buy
            NCamount = NC_obj.amount
            if transaction == "Zakup":
                print(((NCamount*NCprice)+(price*amount))/(NCamount+amount))
                NC_obj.price_buy = ((NCamount*NCprice)+(price*amount))/(NCamount+amount)
                NC_obj.amount = NCamount + amount
            else:
                NC_obj.price_buy = ((NCamount*NCprice)-(price*amount))/(NCamount-amount)
                NC_obj.amount = NCamount - amount
            NC_obj.save()

        else:
            if self.genre == "WIG":
                obj = Stocks.objects.create(user=self.request.user,stock=self.NC_stock,broker=self.broker_id,price_buy=price,amount=amount,currency="PLN",last_price=Quotes_last.objects.filter(Name=self.NC_stock).first())
            else:
                obj = NC.objects.create(user=self.request.user,stock=self.NC_stock,broker=self.broker_id,price_buy=price,amount=amount,currency="PLN",last_price=NC_Quotes_last.objects.filter(Name=self.NC_stock).first())
        
        if transaction == "Zakup":
            self.broker_id.cash = self.broker_id.cash -(price*amount)
            self.broker_id.save()
        else:
            self.broker_id.cash = self.broker_id.cash +(price*amount)
            self.broker_id.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
 
        context["stock"] = self.kwargs['stock']
        context["broker"] = self.broker_id
        context["amount"] = self.amount

        return context


class Cash_exchange (LoginRequiredMixin,CreateView):  
    template_name = 'wallet/exchange.html'
    model = Cantor
    fields = ["cash_to","cash_for","day_transfer","exchange_rate","currency_account_for"]
    


    def get_success_url(self):
 
        return reverse("wallet")

    def get_form(self):

        form = super(Cash_exchange, self).get_form()
        account = self.request.GET.get("account_name")
        if account:
            self.request.session['account_name'] = account
    
        account_obj =Currency_account.objects.get(user=self.request.user,name=self.request.session['account_name'])

        form.fields['day_transfer'].widget.attrs.update({'autocomplete': 'off'})
        form.fields['currency_account_for'].widget.attrs.update({'onchange' : "getSelectValue();"})
        form.fields['cash_to'].widget.attrs.update({'placeholder': account_obj.currency,'onchange' : "cash_to_val();"})
        form.fields['cash_for'].widget.attrs.update({'onchange' : "cash_for_val();"})

        form.fields['currency_account_for'].queryset = Currency_account.objects.filter(user = self.request.user).exclude(currency = account_obj.currency)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        transfer_account = Currency_account.objects.get(user = self.request.user,name = self.request.session['account_name'])
        form.instance.currency_account_to = transfer_account
        cash = transfer_account.cash
        average = transfer_account.average_exchange
        cash_add =form.cleaned_data['cash_to']
        exchange_rate =form.cleaned_data['exchange_rate']
        account_to_data= form.cleaned_data["currency_account_for"]

        account_to = Currency_account.objects.get(name =account_to_data)
  
        form.instance.cash_after_for = account_to.cash - form.cleaned_data['cash_for']
        


        self.object = form.save(commit=False)
        transfer_account.cash =  cash + round(cash_add,2)
        transfer_account.average_exchange = (cash*average + cash_add*exchange_rate)/(cash + cash_add)
        transfer_account.save()
        self.object.cash_after = cash + round(cash_add,2)
        self.object.exchange_rate_after = (cash*average + cash_add*exchange_rate)/(cash + cash_add)
        self.object.save()
        account_to.cash = account_to.cash - form.cleaned_data['cash_for']
        account_to.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currency = Currency_account.objects.get(user = self.request.user,name = self.request.session['account_name'])
        context["currency"] = currency.currency

        return context



def Get_Rate(request):

    if request.GET:
        account = request.GET.get('account')
        currency_to = request.GET.get('currency')
        if  not account == '':
            currency_for = Currency_account.objects.get(id = account)
            currency = currency_for.currency

            Currency_rate= CurrencyData.objects.get(Symbol=f'{currency_to}{currency_for.currency}')
            rate = Currency_Last.objects.get(Name = Currency_rate )
            rate_price = round(rate.Closing_price,2)
        else :
            rate_price = ''
            currency = ''

  
    return JsonResponse({'success':True,"currency":currency, "rate":rate_price}, status=200)

def autocomplete(request,pk):
    if 'term' in request.GET:
        Company = CompanyData.objects.filter(
            Q(Name__icontains=request.GET.get('term'))|
            Q(Symbol__icontains=request.GET.get('term'))
            ).distinct()


        NC = NCData.objects.filter(
            Q(Name__icontains=request.GET.get('term'))|
            Q(Symbol__icontains=request.GET.get('term'))
            ).distinct()

        Stocks=list(chain(Company,NC))
        Stocks = serializers.serialize('json', Stocks)
        
    
        return JsonResponse({'success':True,"Stocks":Stocks, }, status=200)
    return render(request, 'wallet/find_stocks.html',{"pk":pk})

class Create_account(LoginRequiredMixin,CreateView):
    model = Currency_account
    template_name = 'wallet/create_account.html'
    fields = ["name","currency"]

    def get_success_url(self):

        return reverse("wallet")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.cash = 0
        form.instance.average_exchange = 0
        return super().form_valid(form)


class AccountDelete(DeleteView):
    model = Currency_account
    template_name = 'wallet/delete_account.html'

    def get_success_url(self):

        return reverse("wallet")


        
   

    

  


    

    