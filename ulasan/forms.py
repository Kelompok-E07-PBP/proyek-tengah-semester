from django.forms import ModelForm
from ulasan.models import UlasanEntry
from django.utils.html import strip_tags

class UlasanEntryForm(ModelForm):
    class Meta:
        model = UlasanEntry
        fields = ["nama_produk_ulas", "rating", "komentar"]
    
    def clean_nama_produk_ulas(self):
        nama_produk_ulas = self.cleaned_data["nama_produk_ulas"]
        return strip_tags(nama_produk_ulas)

    def clean_komentar(self):
        komentar = self.cleaned_data["komentar"]
        return strip_tags(komentar)