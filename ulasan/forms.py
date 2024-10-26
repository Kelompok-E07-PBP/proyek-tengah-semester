from django.forms import ModelForm
from ulasan.models import UlasanEntry

class UlasanEntryForm(ModelForm):
    class Meta:
        model = UlasanEntry
        fields = ["nama_produk_ulas", "rating", "komentar"]