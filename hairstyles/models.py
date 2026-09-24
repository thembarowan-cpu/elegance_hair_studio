from django.db import models

class Hairstyle(models.Model):
    CATEGORY_CHOICES = [
        ('cut', 'Haircuts'),
        ('braid', 'Braiding'),
        ('colour', 'Colouring'),
        ('style', 'Styling'),
        ('beard', 'Beard Grooming'),
    ]
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='hairstyles/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name