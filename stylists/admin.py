from django.contrib import admin
from .models import Stylist, WorkingHours

class WorkingHoursInline(admin.TabularInline):
    model = WorkingHours
    extra = 1

@admin.register(Stylist)
class StylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    inlines = [WorkingHoursInline]

@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('stylist', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'stylist')