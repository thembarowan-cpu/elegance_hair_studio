from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/', views.book, name='book'),
    path('get-times/', views.get_times, name='get_times'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('cancel/<int:pk>/', views.cancel_appointment, name='cancel'),
]