from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.shortcuts import render, redirect
from django.urls import reverse
from edit.forms import ProductForm
from main.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

def is_superuser(user):
    return user.is_superuser

@login_required(login_url='/login')
@user_passes_test(is_superuser, login_url='/edit/forbidden', redirect_field_name=None)
def show_edit_main(request):
    context = {
        'nama_aplikasi': 'Mujur Reborn Admin',
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "edit_main.html", context)

def forbidden_view(request):
    return render(request, "forbidden.html", status=404)

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

def edit_product_entry(request, id):
    product_entry = Product.objects.get(pk = id)
    form = ProductForm(request.POST or None, instance=product_entry)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('edit:show_edit_main'))

    context = {'form': form}
    return render(request, "edit_product_entry.html", context)

def delete_product_entry(request, id):
    product_entry = Product.objects.get(pk = id)
    product_entry.delete()
    return HttpResponseRedirect(reverse('edit:show_edit_main'))

@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    nama_produk = strip_tags(request.POST.get("nama_produk"))
    kategori = strip_tags(request.POST.get("kategori"))
    harga = request.POST.get("harga")
    gambar_produk = request.POST.get("gambar_produk")

    new_product = Product(
        nama_produk=nama_produk, kategori=kategori,
        harga=harga, gambar_produk=gambar_produk,
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)