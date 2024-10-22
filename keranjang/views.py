from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Keranjang, ItemKeranjang
from .forms import TambahKeKeranjangForm, UpdateItemKeranjangForm
from main.models import Product

@login_required
def keranjang_detail(request):
    keranjang, created = Keranjang.objects.get_or_create(user=request.user)
    items = keranjang.itemkeranjang_set.all()
    update_forms = {
        item.id: UpdateItemKeranjangForm(instance=item)
        for item in items
    }
    context = {
        'keranjang': keranjang,
        'update_forms': update_forms,
    }
    return render(request, 'keranjang_detail.html', context)  

@login_required
def tambah_ke_keranjang(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    keranjang, created = Keranjang.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = TambahKeKeranjangForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            item_keranjang, created = ItemKeranjang.objects.get_or_create(
                keranjang=keranjang,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                item_keranjang.quantity += quantity
                item_keranjang.save()
            
            messages.success(request, f"{product.nama_produk} ditambahkan ke keranjang")
            return redirect('keranjang_detail')
    else:
        form = TambahKeKeranjangForm()
    
    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'tambah_ke_keranjang.html', context)  

@login_required
def update_keranjang(request, item_id):
    item_keranjang = get_object_or_404(ItemKeranjang, id=item_id, keranjang__user=request.user)
    
    if request.method == 'POST':
        form = UpdateItemKeranjangForm(request.POST, instance=item_keranjang)
        if form.is_valid():
            form.save()
            messages.success(request, "Keranjang berhasil diperbarui")
        else:
            messages.error(request, "Gagal memperbarui keranjang")
    
    return redirect('keranjang_detail')

@login_required
def hapus_dari_keranjang(request, item_id):
    item_keranjang = get_object_or_404(ItemKeranjang, id=item_id, keranjang__user=request.user)
    item_keranjang.delete()
    messages.success(request, "Item dihapus dari keranjang")
    return redirect('keranjang_detail')

@login_required
def checkout(request):
    keranjang = get_object_or_404(Keranjang, user=request.user)
    if keranjang.itemkeranjang_set.count() == 0:
        messages.error(request, "Keranjang belanja kosong")
        return redirect('keranjang_detail')
    
    return redirect('payment_page')