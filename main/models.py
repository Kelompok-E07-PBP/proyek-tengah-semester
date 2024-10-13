from django.db import models

class Produk(models.Model):
    nama_produk = models.CharField(max_length=255)
    kategori = models.CharField(max_length=255)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    gambar_produk = models.URLField(max_length=200)
