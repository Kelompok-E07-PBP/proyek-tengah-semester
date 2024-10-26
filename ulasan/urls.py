from django.urls import path
from ulasan.views import show_ulasan_main, create_ulasan_entry, show_json, edit_ulasan, delete_ulasan

app_name = 'ulasan'

urlpatterns = [
    path('', show_ulasan_main, name='show_ulasan_main'),
    path('create-ulasan-entry', create_ulasan_entry, name='create_ulasan_entry'),
    path('json/', show_json, name='show_json'),
    path('edit-ulasan/<uuid:id>', edit_ulasan, name='edit_ulasan'),
    path('delete/<uuid:id>', delete_ulasan, name='delete_ulasan'),
]