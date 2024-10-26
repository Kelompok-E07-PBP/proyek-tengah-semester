from django.urls import path
from pengiriman.views import pengiriman_view, show_json, process_pengiriman_ajax

app_name = 'pengiriman'

urlpatterns = [
    path('pengiriman/', pengiriman_view, name='pengiriman'), 
    path('json/', show_json, name='show_json_pengiriman'),
    path('process_pengiriman_ajax/', process_pengiriman_ajax, name='process_pengiriman_ajax'),
]