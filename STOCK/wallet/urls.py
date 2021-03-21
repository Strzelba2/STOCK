from django.urls import path
from .views import wallet,Cash_Deposit,Cash_withdrawal,Lista_Bank_transfer,Cash_exchange,Get_Rate,Create_account,AccountDelete,Lista_Stocks,buy_stocks,buy_NC,autocomplete



urlpatterns = [
    path('wallet/', wallet.as_view() ,name='wallet'),
    path('Cash_Deposit/', Cash_Deposit.as_view() ,name='Cash_Deposit'),
    path('Cash_withdrawal/', Cash_withdrawal.as_view() ,name='Cash_withdrawal'),
    path('Lista_Bank_transfer/', Lista_Bank_transfer.as_view() ,name='Lista_Bank_transfer'),
    path('Cash_exchange/', Cash_exchange.as_view() ,name='Cash_exchange'),
    path('Create_account/', Create_account.as_view() ,name='Create_account'),
    path('AccountDelete/<int:pk>/', AccountDelete.as_view() ,name='AccountDelete'),
    path('Get_Rate/', Get_Rate ,name='Get_Rate'),
    path('Lista_Stocks/<int:pk>', Lista_Stocks.as_view() ,name='Lista_Stocks'),
    path('Lista_Stocks/<int:pk>/auto/', autocomplete ,name='autocomplete'),
    path('Lista_Stocks/<int:pk>/buy_stocks/<str:stock>/<str:genre>/', buy_stocks.as_view() ,name='buy_stocks'),

]