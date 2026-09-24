from django.shortcuts import render
from .models import Hairstyle

def hairstyle_list(request):
    qs = Hairstyle.objects.all()
    category = request.GET.get('category')
    search = request.GET.get('q')
    if category:
        qs = qs.filter(category=category)
    if search:
        qs = qs.filter(name__icontains=search)
    return render(request, 'hairstyles/list.html', {
        'hairstyles': qs,
        'categories': Hairstyle.CATEGORY_CHOICES,
        'selected_category': category,
        'search_query': search or '',
    })