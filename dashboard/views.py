from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count
from bookings.models import Appointment
from datetime import date

def is_staff(user):
    return user.is_staff

@login_required
def customer_dashboard(request):
    upcoming = request.user.appointments.filter(
        date__gte=date.today(),
        status__in=['pending', 'confirmed']
    )
    past = request.user.appointments.exclude(
        date__gte=date.today(),
        status__in=['pending', 'confirmed']
    )
    return render(request, 'dashboard/customer.html', {
        'upcoming': upcoming,
        'past': past,
    })

@login_required
@user_passes_test(is_staff)
def admin_dashboard(request):
    total = Appointment.objects.count()
    confirmed = Appointment.objects.filter(status='confirmed').count()
    cancelled = Appointment.objects.filter(status='cancelled').count()
    completed = Appointment.objects.filter(status='completed').count()
    upcoming = Appointment.objects.filter(
        date__gte=date.today(),
        status__in=['pending', 'confirmed']
    ).count()
    by_stylist = list(Appointment.objects.values('stylist__name').annotate(count=Count('id')).order_by('-count'))
    by_service = list(Appointment.objects.values('service__name').annotate(count=Count('id')).order_by('-count'))
    recent = Appointment.objects.select_related('customer', 'service', 'stylist')[:15]

    return render(request, 'dashboard/admin_home.html', {
        'total': total,
        'confirmed': confirmed,
        'cancelled': cancelled,
        'completed': completed,
        'upcoming': upcoming,
        'by_stylist': by_stylist,
        'by_service': by_service,
        'recent': recent,
    })

@login_required
@user_passes_test(is_staff)
def manage_appointments(request):
    appointments = Appointment.objects.select_related('customer', 'service', 'stylist').all()
    return render(request, 'dashboard/manage_appointments.html', {'appointments': appointments})

@login_required
@user_passes_test(is_staff)
def update_appointment_status(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appt.status = new_status
            appt.save()
            messages.success(request, 'Appointment status updated.')
    return redirect('dashboard:manage_appointments')