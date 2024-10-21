from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect   # Tambahkan import redirect di baris ini
from edit.forms import ProductForm
from main.models import Product

def show_edit_main(request):
    product_entries = Product.objects.all()
    context = {
        'nama_aplikasi': 'Mujur Reborn Admin',
        'product_entries' : product_entries,
    }

    return render(request, "edit_main.html", context)

def create_product_entry(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('edit:show_edit_main')

    context = {'form': form}
    return render(request, "create_product_entry.html", context)


def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
