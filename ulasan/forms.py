from django import forms 
#Mengimpor modul forms dari Django. Modul ini menyediakan berbagai fungsi dan kelas untuk membuat dan memproses form HTML di Django, seperti validasi data dan pembuatan form berbasis model.
from .models import Ulasan 
#Mengimpor model Ulasan dari file models.py di aplikasi yang sama. Model ini akan digunakan sebagai dasar untuk membuat form yang otomatis berhubungan dengan field-field yang ada pada model Ulasan.

class UlasanForm(forms.ModelForm): #Buat kelas UlasanForm yang merupakan subclass dari forms.ModelForm
    class Meta: #Mendefinisikan metadata yang berkaitan dengan form
        model = Ulasan #model berbasis pada model Ulasan
        fields = ['nama_pengguna', 'rating', 'komentar'] #Field diambil dari models.py
