from django.urls import path
from . import views
from keranjang.views import keranjang_detail, tambah_ke_keranjang, hapus_dari_keranjang, update_keranjang, checkout, tambah_ke_keranjang_ajax, update_keranjang_ajax, hapus_dari_keranjang_ajax

urlpatterns = [
    path('keranjang/', keranjang_detail, name='keranjang_detail'),
    path('tambah-ke-keranjang/<uuid:product_id>/', tambah_ke_keranjang, name='tambah_ke_keranjang'),
    path('hapus/<int:item_id>/', hapus_dari_keranjang, name='hapus_dari_keranjang'),
    path('update/<int:item_id>/', update_keranjang, name='update_keranjang'),
    path('checkout/', checkout, name='checkout'),
    path('tambah-ke-keranjang-ajax/<str:product_id>/', tambah_ke_keranjang_ajax, name='tambah_ke_keranjang_ajax'),
    path('update-keranjang-ajax/<int:item_id>/', update_keranjang_ajax, name='update_keranjang_ajax'),
    path('hapus-dari-keranjang-ajax/<int:item_id>/', hapus_dari_keranjang_ajax, name='hapus_dari_keranjang_ajax')
]