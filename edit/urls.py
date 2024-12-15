from django.urls import path
from edit.views import show_edit_main, create_product_entry, show_json, forbidden_view, edit_product_entry
from edit.views import delete_product_entry, add_product_entry_ajax, create_product_flutter
from edit.views import delete_product_entry_flutter

app_name = 'edit'

urlpatterns = [
    path('', show_edit_main, name='show_edit_main'),
    path('create-product-entry', create_product_entry, name='create_product_entry'),
    path('json/', show_json, name='show_json'),
    path('forbidden/', forbidden_view, name='forbidden_view'),
    path('edit-product-entry/<uuid:id>', edit_product_entry, name='edit_product_entry'),
    path('delete/<uuid:id>', delete_product_entry, name='delete_product_entry'),
    path('create-product-entry-ajax', add_product_entry_ajax, name='add_product_entry_ajax'),
    path('create-product-flutter/', create_product_flutter, name='create_product_flutter'),
    path('delete-from-flutter/<str:id>', delete_product_entry_flutter, name='delete_from_flutter')
]