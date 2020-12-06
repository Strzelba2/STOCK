from django.urls import path
from .views import wallet



urlpatterns = [
    path('wallet/', wallet ,name='wallet'),

]