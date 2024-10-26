from django.urls import path
from ulasan.views import show_ulasan_main, create_ulasan_entry, show_json

app_name = 'ulasan'

urlpatterns = [
    path('', show_ulasan_main, name='show_ulasan_main'),
    path('create-ulasan-entry', create_ulasan_entry, name='create_ulasan_entry'),
    path('json/', show_json, name='show_json'),
]