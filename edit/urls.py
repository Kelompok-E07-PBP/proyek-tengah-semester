from django.urls import path
from edit.views import show_edit_main, create_product_entry, show_json, forbidden_view, edit_product_entry
from edit.views import delete_product_entry

app_name = 'edit'

urlpatterns = [
    path('', show_edit_main, name='show_edit_main'),
    path('create-product-entry', create_product_entry, name='create_product_entry'),
    path('json/', show_json, name='show_json'),
    path('forbidden/', forbidden_view, name='forbidden_view'),
    path('edit-product-entry/<uuid:id>', edit_product_entry, name='edit_product_entry'),
    path('delete/<uuid:id>', delete_product_entry, name='delete_product_entry'),
]