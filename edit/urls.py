from django.urls import path
from edit.views import show_edit_main, create_product_entry, show_json, forbidden_view

app_name = 'edit'

urlpatterns = [
    path('', show_edit_main, name='show_edit_main'),
    path('create-product-entry', create_product_entry, name='create_product_entry'),
    path('json/', show_json, name='show_json'),
    path('forbidden/', forbidden_view, name='forbidden_view')
]