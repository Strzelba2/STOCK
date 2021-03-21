from django.urls import path
from .views import init_data,update_WIG,Home,Analysis,update_Index,update_Currency,update_Wares,update_NC



urlpatterns = [
    path('init/', init_data,name='init_data'),
    path('update_NC/', update_NC,name='update_NC'),
    path('update_WIG/', update_WIG,name='update_WIG'),
    path('update_Index/', update_Index,name='update_Index'),
    path('update_Wares/', update_Wares,name='update_Wares'),
    path('update_Currency/', update_Currency,name='update_Currency'),
    path('', Home.as_view(),name='home'),
    path('Analysis', Analysis.as_view(),name='Analysis'),
    #path('Chart_data/<str:name>/', Chart_data.as_view(),name='Chart_data'),

]