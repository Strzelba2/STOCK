from django.urls import path
from .views import init_data,update_data,Home



urlpatterns = [
    path('init/', init_data,name='init_data'),
    path('update/', update_data,name='update_data'),
    path('', Home.as_view(),name='home'),

]