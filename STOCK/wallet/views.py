from django.shortcuts import render

# Create your views here.


def wallet(request, *args, **kwargs):

    return render(request, "wallet/wallet.html")