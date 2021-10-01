from django.contrib import admin
from django.urls import path, include

from ajworldapp import views

urlpatterns = [
    path('', views.index,name='index'),   
    path('pdf/', views.pdf,name='pdf'),
    path('empty_data/', views.empty_data,name='empty_data'),

    
    
]