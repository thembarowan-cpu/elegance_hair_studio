from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, date
from services.models import Service
from stylists.models import Stylist
from .models import Appointment
from .utils import get_available_slots, is_slot_available

@login_required
def book(request):
    services = Service.objects.filter(is_active=True)
    stylists = Stylist.objects.filter(is_active=True)

    if request.method == 'POST':
        try:
            service = get_object_or_404(Service, id=request.POST.get('service'), is_active=True)
            stylist = get_object_or_404(Stylist, id=request.POST.get('stylist'), is_active=True)
            date_obj = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
            start_time = datetime.strptime(request.POST.get('time'), '%H:%M').time()
            special = request.POST.get('special_requests', '')

            available, result = is_slot_available(stylist, service, date_obj, start_time)
            if not available:
                messages.error(request, result)
                return redirect('bookings:book')

            Appointment.objects.create(
                customer=request.user,
                service=service,
                stylist=stylist,
                date=date_obj,
                start_time=start_time,
                end_time=result,
                special_requests=special,
                status='confirmed'
            )
            messages.success(request, 'Your appointment has been booked successfully!')
            return redirect('bookings:confirmation')
        except Exception:
            messages.error(request, 'Something went wrong. Please try again.')
            return redirect('bookings:book')

    return render(request, 'bookings/book.html', {
        'services': services,
        'stylists': stylists,
        'today': date.today().isoformat(),
    })

@login_required
def get_times(request):
    stylist_id = request.GET.get('stylist')
    service_id = request.GET.get('service')
    date_str = request.GET.get('date')
    if not all([stylist_id, service_id, date_str]):
        return JsonResponse({'times': []})
    try:
        stylist = Stylist.objects.get(id=stylist_id, is_active=True)
        service = Service.objects.get(id=service_id, is_active=True)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        slots = get_available_slots(stylist, service, date_obj)
        return JsonResponse({'times': [t.strftime('%H:%M') for t in slots]})
    except Exception:
        return JsonResponse({'times': []})

@login_required
def confirmation(request):
    return render(request, 'bookings/confirmation.html')

@login_required
def my_appointments(request):
    appointments = request.user.appointments.all()
    return render(request, 'bookings/my_appointments.html', {'appointments': appointments})

@login_required
def cancel_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, customer=request.user)
    if appt.status in ['pending', 'confirmed']:
        appt.status = 'cancelled'
        appt.save()
        messages.success(request, 'Appointment cancelled successfully.')
    else:
        messages.error(request, 'This appointment cannot be cancelled.')
    return redirect('bookings:my_appointments')