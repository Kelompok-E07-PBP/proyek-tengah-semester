from django import forms
from pengiriman.models import Pengiriman

class PengirimanForm(forms.ModelForm):
    class Meta:
        model = Pengiriman
        fields = ['address', 'city', 'postal_code', 'courier']