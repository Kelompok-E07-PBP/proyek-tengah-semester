from django.urls import path
from pengiriman.views import pengiriman_view, show_json

urlpatterns = [
    path('', pengiriman_view, name='pengiriman'),
    path('json/', show_json, name='show_json_pengiriman'),
]