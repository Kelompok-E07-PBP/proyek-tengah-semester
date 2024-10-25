from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Keranjang, ItemKeranjang
from .forms import TambahKeKeranjangForm, UpdateItemKeranjangForm
from main.models import Product
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import logging
import uuid

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
        try:
            new_quantity = int(request.POST.get('quantity', 1))
            if new_quantity > 0:
                item_keranjang.quantity = new_quantity
                item_keranjang.save()
                messages.success(request, "Keranjang berhasil diperbarui")
            else:
                messages.error(request, "Jumlah harus lebih dari 0")
        except (ValueError, TypeError):
            messages.error(request, "Jumlah tidak valid")
    
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

logger = logging.getLogger(__name__)

@login_required
@require_POST
def tambah_ke_keranjang_ajax(request, product_id):
    try:
        # Convert string UUID to UUID object
        product_uuid = uuid.UUID(product_id)
        
        # Get the product using the UUID
        product = get_object_or_404(Product, id=product_uuid)
        keranjang, created = Keranjang.objects.get_or_create(user=request.user)
        
        # Get quantity from POST data
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'Jumlah produk tidak valid'
            }, status=400)
        
        if quantity <= 0:
            return JsonResponse({
                'success': False,
                'message': 'Quantity harus lebih dari 0'
            }, status=400)
            
        item_keranjang, created = ItemKeranjang.objects.get_or_create(
            keranjang=keranjang,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            item_keranjang.quantity += quantity
            item_keranjang.save()
        
        return JsonResponse({
            'success': True,
            'message': f"{product.nama_produk} berhasil ditambahkan ke keranjang",
            'cart_count': keranjang.itemkeranjang_set.count()
        })
        
    except ValueError as e:
        # Invalid UUID format
        return JsonResponse({
            'success': False,
            'message': 'ID produk tidak valid'
        }, status=400)
    except Exception as e:
        print(f"Error: {str(e)}")  # For debugging
        return JsonResponse({
            'success': False,
            'message': 'Gagal menambahkan produk ke keranjang'
        }, status=400)