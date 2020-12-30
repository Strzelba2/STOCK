from django.urls import path
from .views import init_data,update_data,Home,Analysis,Chart_data



urlpatterns = [
    path('init/', init_data,name='init_data'),
    path('update/', update_data,name='update_data'),
    path('', Home.as_view(),name='home'),
    path('Analysis', Analysis.as_view(),name='Analysis'),
    path('Chart_data/<str:name>/', Chart_data.as_view(),name='Chart_data'),

]