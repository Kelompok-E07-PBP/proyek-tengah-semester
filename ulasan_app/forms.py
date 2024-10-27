from django import forms
from .models import Ulasan

class UlasanForm(forms.ModelForm):
    class Meta:
        model = Ulasan
        fields = ['product_name', 'rating', 'likes', 'dislikes']