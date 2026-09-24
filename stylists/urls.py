from django.urls import path
from . import views

app_name = 'stylists'

urlpatterns = [
    path('', views.stylist_list, name='list'),
]