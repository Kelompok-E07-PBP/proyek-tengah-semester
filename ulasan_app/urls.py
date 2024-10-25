from django.urls import path
from .views import ulasan_list, create_ulasan

urlpatterns = [
    path('', ulasan_list, name='ulasan_list'),
    path('create/', create_ulasan, name='create_ulasan'),
]