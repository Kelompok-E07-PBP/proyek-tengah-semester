from django import forms
from pengiriman.models import Pengiriman

class PengirimanForm(forms.ModelForm):
    class Meta:
        model = Pengiriman
        fields = ['first_name','last_name','email','phone_number','address', 'city', 'postal_code', 'courier']
        labels = {
            'first_name': 'Nama Depan',
            'last_name': 'Nama Belakang',
            'phone_number': 'Nomor Telepon',
            'address': 'Alamat',
            'city': 'Kota',
            'postal_code': 'Kode Pos',
            'courier': 'Kurir',
        }