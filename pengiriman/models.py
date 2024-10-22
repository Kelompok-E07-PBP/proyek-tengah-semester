from django.db import models
from django.contrib.auth.models import User
class Pengiriman(models.Model):
    COURIER_CHOICES = [
        ('JNE', 'JNE'),
        ('SICEPAT', 'SiCepat'),
        ('GOJEK', 'Gojek'),
        ('GRAB', 'Grab'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    courier = models.CharField(max_length=100, choices=COURIER_CHOICES)