from django.urls import path
from main.views import show_main, register, login_user, logout_user, show_json


app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('json/', show_json, name='show_json'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]