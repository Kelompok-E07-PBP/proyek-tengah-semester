from django.urls import path
from . import views
from keranjang.views import keranjang_detail, tambah_ke_keranjang, hapus_dari_keranjang, update_keranjang, checkout

urlpatterns = [
    path('keranjang/', keranjang_detail, name='keranjang_detail'),
    path('tambah/<uuid:product_id>/', tambah_ke_keranjang, name='tambah_ke_keranjang'),
    path('hapus/<int:item_id>/', hapus_dari_keranjang, name='hapus_dari_keranjang'),
    path('update/<int:item_id>/', update_keranjang, name='update_keranjang'),
    path('checkout/', checkout, name='checkout'),
]