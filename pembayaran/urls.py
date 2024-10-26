from django.urls import path
from pembayaran.views import pembayaran_view, show_json, process_payment_ajax

app_name = 'pembayaran'

urlpatterns = [
    path('pembayaran/process/', process_payment_ajax, name='process_payment_ajax'),
    path('pembayaran/', pembayaran_view, name='pembayaran_view'),
    path('json/', show_json, name='show_json_pembayaran'),
]