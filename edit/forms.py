from django.forms import ModelForm
from main.models import Product
from django.utils.html import strip_tags

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["nama_produk", "kategori", "harga", "gambar_produk"]
    
    def clean_nama_produk(self):
        nama_produk = self.cleaned_data["nama_produk"]
        return strip_tags(nama_produk)

    def clean_kategori(self):
        kategori = self.cleaned_data["kategori"]
        return strip_tags(kategori)