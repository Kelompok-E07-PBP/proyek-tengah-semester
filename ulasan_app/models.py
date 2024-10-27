from django.db import models
from django.contrib.auth.models import User

RATE_CHOICES = [
    (1, '1-Very Poor'),
    (2, '2-Poor'),
    (3, '3-Average'),
    (4, '4-Good'),
    (5, '5-Beyond Average'),
]

class Ulasan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)  # Nama produk
    date = models.DateTimeField(auto_now_add=True)  # Tanggal
    rating = models.PositiveIntegerField(choices=RATE_CHOICES)  # Rating
    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.product_name} - {self.rating}, {self.date}'