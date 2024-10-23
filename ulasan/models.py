from django.db import models

# Create your models here.
class Ulasan(models.Model):
    nama_pengguna=models.CharField(max_length=100) #Nama Pengguna maksimal 10 kata
    rating=models.FloatField() #Rating direpresentasikan dalam float
    komentar=models.TextField() #Komentar direpresentasikan dalam Teks
    tanggal_ulasan=models.DateTimeField(auto_now_add=True) #Mengambil waktu saat ini

    def __str__(self): #Representasikan dalam bentuk string dengan tampilan nama pengguna dan rating materi DDP1
        return f"{self.nama_pengguna}- {self.rating}/5"