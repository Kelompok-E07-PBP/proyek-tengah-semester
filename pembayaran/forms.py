from django import forms
from .models import Pembayaran

class PembayaranForm(forms.ModelForm):
    class Meta:
        model = Pembayaran
        fields = ['payment_method']
