from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'stylist', 'date', 'start_time', 'status')
    list_filter = ('status', 'date', 'stylist')
    search_fields = ('customer__username', 'customer__email', 'service__name')
    date_hierarchy = 'date'