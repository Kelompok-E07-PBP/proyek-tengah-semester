from django.urls import path
from .views import ulasan_app, create_ulasan, hapus_ulasan, show_json, show_json_ajax

urlpatterns = [
    path('', ulasan_app, name='ulasan_app'),
    path('create/', create_ulasan, name='create_ulasan'),
    path('hapus/<int:ulasan_id>/', hapus_ulasan, name='hapus_ulasan'),
    path('json/', show_json, name='show_json'),
    path('ajax/json/', show_json_ajax, name='show_json_ajax'),
]