from django.urls import path
from . import views

app_name = 'hairstyles'

urlpatterns = [
    path('', views.hairstyle_list, name='list'),
]