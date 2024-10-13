from django.urls import path
from edit.views import show_main

app_name = 'edit'

urlpatterns = [
    path('', show_main, name='show_main'),
]