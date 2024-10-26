from django.db import models
from django.contrib.auth.models import User
import uuid

class UlasanEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waktu = models.DateTimeField(auto_now_add=True)
    nama_produk_ulas = models.CharField(max_length=255)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    komentar = models.TextField()