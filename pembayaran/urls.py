from django.urls import path
from pembayaran.views import pembayaran_view, show_json
urlpatterns = [
    path('payment/<int:product_id>/', pembayaran_view, name='pembayaran_view'),
    path('json/', show_json, name='show_json_pembayaran'),
]