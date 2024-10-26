from django.db import models
from django.contrib.auth.models import User

class Pembayaran(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]

    
    METHOD_CHOICES = [
        ('Kartu Kredit', 'Kartu Kredit'),
        ('Kartu Debit', 'Kartu Debit'),
        ('Transfer Bank', 'Transfer Bank'),
        ('E-Wallet', 'E-Wallet'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100, choices=METHOD_CHOICES)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Pembayaran {self.id} - {self.user.username} - {self.amount} IDR'   
    
