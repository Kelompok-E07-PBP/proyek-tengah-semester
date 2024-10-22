from django import forms
from .models import ItemKeranjang

class TambahKeKeranjangForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label='Jumlah'
    )

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 1:
            raise forms.ValidationError("Jumlah minimal adalah 1")
        return quantity

class UpdateItemKeranjangForm(forms.ModelForm):
    class Meta:
        model = ItemKeranjang
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'min': '1',
                'onchange': 'this.form.submit()'
            })
        }

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 1:
            raise forms.ValidationError("Jumlah minimal adalah 1")
        return quantity