from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('customer/', views.customer_dashboard, name='customer'),
    path('admin/', views.admin_dashboard, name='admin'),
    path('admin/appointments/', views.manage_appointments, name='manage_appointments'),
    path('admin/appointments/<int:pk>/status/', views.update_appointment_status, name='update_status'),
]