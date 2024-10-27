from rest_framework import serializers
from .models import UlasanEntry

class UlasanEntrySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UlasanEntry
        fields = ['id', 'username', 'waktu', 'nama_produk_ulas', 'rating', 'komentar']
