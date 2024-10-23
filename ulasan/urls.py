from django.urls import path
from . import views

urlpatterns = [
    path('', views.daftar_ulasan, name='daftar_ulasan'),
    path('tambah/', views.tambah_ulasan, name='tambah_ulasan'),
]