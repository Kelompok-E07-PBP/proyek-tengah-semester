from django.http import HttpResponse, HttpResponseForbidden
from django.core import serializers
from django.shortcuts import render, redirect   # Tambahkan import redirect di baris ini
from edit.forms import ProductForm
from main.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def is_superuser(user):
    return user.is_superuser

@login_required(login_url='/login')
@user_passes_test(is_superuser, login_url='/edit/forbidden', redirect_field_name=None)
def show_edit_main(request):
    product_entries = Product.objects.all()
    context = {
        'nama_aplikasi': 'Mujur Reborn Admin',
        'product_entries' : product_entries,
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
