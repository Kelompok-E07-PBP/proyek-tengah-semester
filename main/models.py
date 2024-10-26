from django.db import models
import uuid

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Dasi Instant', 'Dasi Instant'),
        ('Dasi Manual', 'Dasi Manual'),
        ('Dasi Kupu-Kupu', 'Dasi Kupu-Kupu'),
        ('Jepitan Dasi', 'Jepitan Dasi'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_produk = models.CharField(max_length=255)
    kategori = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    gambar_produk = models.URLField(max_length=200)
