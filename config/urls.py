from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('services/', include('services.urls')),
    path('hairstyles/', include('hairstyles.urls')),
    path('stylists/', include('stylists.urls')),
    path('accounts/', include('accounts.urls')),
    path('bookings/', include('bookings.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('policies/', TemplateView.as_view(template_name='policies.html'), name='policies'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)