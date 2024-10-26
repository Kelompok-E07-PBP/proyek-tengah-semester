from django.urls import path
from main.views import show_main, register, login_user, logout_user, show_json, forbidden_view_main


app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('json/', show_json, name='show_json'),
    path('forbidden/', forbidden_view_main, name='forbidden_view_main'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]