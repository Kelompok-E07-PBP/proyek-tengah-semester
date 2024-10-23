from django.shortcuts import render, redirect
 #Render: Fungsi ini digunakan untuk merender template HTML dengan data dari view ke dalam response HTTP
 #redirect: Fungsi ini digunakan untuk mengalihkan pengguna ke URL atau view lain setelah suatu aksi (misalnya, setelah form berhasil disubmit).

from .models import Ulasan
#Mengimport model Ulasan dari file models.py dalam applikasi yang sama (app Ulasan)

from .forms import UlasanForm

#Create Views Here
def daftar_ulasan(request): #Mendefinisikan sebuah view bernama daftar_ulasan yang menerima parameter request. View ini digunakan untuk menangani permintaan HTTP dari pengguna, khususnya untuk menampilkan daftar ulasan yang ada di database.
    ulasan=Ulasan.objects.all() #engambil semua objek (ulasan) yang ada dalam model Ulasan dari database menggunakan Ulasan.objects.all(). Ini menghasilkan daftar (queryset) dari semua ulasan yang telah disimpan.
    return render(request,'daftar_ulasan.html',{'ulasan': ulasan}) #Fungsi render digunakan untuk merender template daftar_ulasan.html.


def tambah_ulasan(request):
    if request.method=='POST': #Memeriksa apakah metode permintaan HTTP yang diterima adalah POST. Jika POST, berarti pengguna telah mengirimkan data form (misalnya, setelah mengisi form dan menekan tombol submit).
        form=UlasanForm(request.POST) #Membuat instance form UlasanForm dan mengisi dengan data yang dikirimkan melalui request.POST. Data ini berisi input dari pengguna yang berasal dari form ulasan.
        if form.is_valid(): #Mengecek apakah data yang dimasukkan ke dalam form valid sesuai dengan aturan yang ada di model (misalnya, apakah field wajib terisi, apakah format rating benar, dll.). Jika valid, eksekusi akan dilanjutkan.
            form.save() #Jika form valid, data ulasan baru akan disimpan ke database. Django secara otomatis membuat objek baru di tabel Ulasan dengan menggunakan data yang dikirimkan dalam form.
            return redirect('daftar_ulasan') #Setelah ulasan berhasil disimpan, pengguna akan diarahkan (redirect) ke halaman daftar ulasan (daftar_ulasan). Ini untuk mencegah form disubmit ulang jika pengguna merefresh halaman setelah menambahkan ulasan.

    #Jika metode permintaan bukan POST (misalnya, GET), fungsi akan membuat instance form kosong (UlasanForm()) untuk ditampilkan kepada pengguna. 
    # Hal ini memungkinkan pengguna untuk melihat form kosong sebelum mereka mulai mengisi ulasan.  
    else:
        form=UlasanForm()
    return render(request,'tambah_ulasan.html',{'form':form})

