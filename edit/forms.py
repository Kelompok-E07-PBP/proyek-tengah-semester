from django.forms import ModelForm
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["nama_produk", "kategori", "harga", "gambar_produk"]