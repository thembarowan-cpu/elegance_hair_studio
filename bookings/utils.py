from datetime import datetime, timedelta
from .models import Appointment
from stylists.models import WorkingHours

def get_available_slots(stylist, service, date):
    duration = timedelta(minutes=service.duration_minutes)
    day = date.weekday()

    try:
        hours = WorkingHours.objects.get(stylist=stylist, day_of_week=day)
    except WorkingHours.DoesNotExist:
        return []

    existing = Appointment.objects.filter(
        stylist=stylist,
        date=date,
        status__in=['pending', 'confirmed']
    ).order_by('start_time')

    slots = []
    current = datetime.combine(date, hours.start_time)
    end_of_day = datetime.combine(date, hours.end_time)

    while current + duration <= end_of_day:
        slot_end = current + duration
        conflict = False
        for appt in existing:
            appt_start = datetime.combine(date, appt.start_time)
            appt_end = datetime.combine(date, appt.end_time)
            if current < appt_end and slot_end > appt_start:
                conflict = True
                break
        if not conflict:
            slots.append(current.time())
        current += timedelta(minutes=15)

    return slots

def is_slot_available(stylist, service, date, start_time):
    duration = timedelta(minutes=service.duration_minutes)
    end_dt = datetime.combine(date, start_time) + duration
    end_time = end_dt.time()

    day = date.weekday()
    try:
        hours = WorkingHours.objects.get(stylist=stylist, day_of_week=day)
        if start_time < hours.start_time or end_time > hours.end_time:
            return False, "Selected time is outside the stylist's working hours."
    except WorkingHours.DoesNotExist:
        return False, "Stylist is not available on this day."

    conflicts = Appointment.objects.filter(
        stylist=stylist,
        date=date,
        status__in=['pending', 'confirmed']
    )
    for appt in conflicts:
        if start_time < appt.end_time and end_time > appt.start_time:
            return False, "That appointment time is no longer available. Please select another time."

    return True, end_time