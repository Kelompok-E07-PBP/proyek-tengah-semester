from django import forms
from pengiriman.models import Pengiriman

class PengirimanForm(forms.ModelForm):
    class Meta:
        model = Pengiriman
        fields = ['address', 'city', 'postal_code', 'courier']
        labels = {
            'address': 'Alamat',
            'city': 'Kota',
            'postal_code': 'Kode Pos',
            'courier': 'Kurir',
        }