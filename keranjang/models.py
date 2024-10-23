from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Keranjang(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_total(self):
        return sum(item.get_subtotal() for item in self.itemkeranjang_set.all())
    
    def __str__(self):
        return f"Keranjang - {self.user.username}"

class ItemKeranjang(models.Model):
    keranjang = models.ForeignKey(Keranjang, on_delete=models.CASCADE)
    product = models.ForeignKey('main.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_subtotal(self):
        return self.product.harga * self.quantity
    
    def __str__(self):
        return f"{self.product.nama_produk} ({self.quantity})"