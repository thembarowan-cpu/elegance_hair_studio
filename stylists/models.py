from django.db import models

class Stylist(models.Model):
    ROLE_CHOICES = [
        ('senior', 'Senior Stylist'),
        ('colour', 'Colour Specialist'),
        ('junior', 'Junior Stylist'),
        ('barber', 'Barber / Beard Specialist'),
    ]
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='senior')
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='stylists/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"

class WorkingHours(models.Model):
    DAYS = [
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
        (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday'),
    ]
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE, related_name='working_hours')
    day_of_week = models.IntegerField(choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ['stylist', 'day_of_week']
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.stylist.name} - {self.get_day_of_week_display()}"