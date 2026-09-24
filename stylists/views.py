from django.shortcuts import render
from .models import Stylist

def stylist_list(request):
    stylists = Stylist.objects.filter(is_active=True).prefetch_related('working_hours')
    return render(request, 'stylists/list.html', {'stylists': stylists})