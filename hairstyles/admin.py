from django.contrib import admin
from .models import Hairstyle

@admin.register(Hairstyle)
class HairstyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name',)