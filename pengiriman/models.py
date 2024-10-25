from django.db import models
from django.contrib.auth.models import User
class Pengiriman(models.Model):
    COURIER_CHOICES = [
        ('JNE', 'JNE'),
        ('SICEPAT', 'SiCepat'),
        ('GOJEK', 'Gojek'),
        ('GRAB', 'Grab'),
    ]

    CITY_CHOICES = [
        ('Jakarta Barat', 'Jakarta Barat'),
        ('Jakarta Pusat', 'Jakarta Pusat'),
        ('Jakarta Selatan', 'Jakarta Selatan'),
        ('Jakarta Timur', 'Jakarta Timur'),
        ('Jakarta Utara', 'Jakarta Utara'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.IntegerField()
    address = models.TextField()
    city = models.CharField(max_length=100, choices=CITY_CHOICES)
    postal_code = models.IntegerField()
    courier = models.CharField(max_length=100, choices=COURIER_CHOICES)