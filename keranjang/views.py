from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Keranjang, ItemKeranjang
from .forms import TambahKeKeranjangForm, UpdateItemKeranjangForm
from main.models import Product
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponseRedirect
import logging
import uuid
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='/login')
@csrf_exempt
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

@login_required(login_url='/login')
@csrf_exempt
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

@login_required(login_url='/login')
@csrf_exempt
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

@login_required(login_url='/login')
@csrf_exempt
def hapus_dari_keranjang(request, item_id):
    item_keranjang = get_object_or_404(ItemKeranjang, id=item_id, keranjang__user=request.user)
    item_keranjang.delete()
    messages.success(request, "Item dihapus dari keranjang")
    return redirect('keranjang_detail')

@login_required(login_url='/login')
@csrf_exempt
def checkout(request):
    keranjang = get_object_or_404(Keranjang, user=request.user)
    if keranjang.itemkeranjang_set.count() == 0:
        messages.error(request, "Keranjang belanja kosong")
        return redirect('keranjang_detail')
    
    url = reverse('pengiriman:pengiriman') + f'?keranjang_id={keranjang.id}'
    return HttpResponseRedirect(url)


logger = logging.getLogger(__name__)

@login_required(login_url='/login')
@csrf_exempt
@require_POST
def tambah_ke_keranjang_ajax(request, product_id):
    try:
        product_uuid = uuid.UUID(product_id)
        
        product = get_object_or_404(Product, id=product_uuid)
        keranjang, created = Keranjang.objects.get_or_create(user=request.user)

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
        return JsonResponse({
            'success': False,
            'message': 'ID produk tidak valid'
        }, status=400)
    except Exception as e:
        print(f"Error: {str(e)}") 
        return JsonResponse({
            'success': False,
            'message': 'Gagal menambahkan produk ke keranjang'
        }, status=400)
    

@login_required(login_url='/login')
@csrf_exempt
@require_POST
def update_keranjang_ajax(request, item_id):
    try:
        item_keranjang = get_object_or_404(ItemKeranjang, id=item_id, keranjang__user=request.user)
        new_quantity = int(request.POST.get('quantity', 1))
        
        if new_quantity <= 0:
            return JsonResponse({
                'success': False,
                'message': 'Jumlah harus lebih dari 0'
            }, status=400)
        
        item_keranjang.quantity = new_quantity
        item_keranjang.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Keranjang berhasil diperbarui',
            'subtotal': item_keranjang.get_subtotal(),
            'total': item_keranjang.keranjang.get_total()
        })
        
    except (ValueError, TypeError):
        return JsonResponse({
            'success': False,
            'message': 'Jumlah tidak valid'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Terjadi kesalahan saat memperbarui keranjang'
        }, status=500)

@login_required(login_url='/login')
@csrf_exempt
@require_POST
def hapus_dari_keranjang_ajax(request, item_id):
    try:
        item_keranjang = get_object_or_404(ItemKeranjang, id=item_id, keranjang__user=request.user)
        keranjang = item_keranjang.keranjang
        item_keranjang.delete()
        
        is_empty = keranjang.itemkeranjang_set.count() == 0
        
        return JsonResponse({
            'success': True,
            'message': 'Item berhasil dihapus dari keranjang',
            'total': keranjang.get_total(),
            'is_empty': is_empty
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Terjadi kesalahan saat menghapus item'
        }, status=500)
    
@login_required(login_url='/login')
@csrf_exempt
def show_json(request):
    keranjang, created = Keranjang.objects.get_or_create(user=request.user)
    items = keranjang.itemkeranjang_set.all()
    
    cart_items = []
    for item in items:
        cart_items.append({
            'id': str(item.id),
            'product_name': item.product.nama_produk,
            'quantity': item.quantity,
            'price': float(item.product.harga),
            'subtotal': float(item.get_subtotal())
        })
    
    data = {
        'username': request.user.username,
        'cart_id': str(keranjang.id),
        'total': float(keranjang.get_total()),
        'items': cart_items,
        'created_at': keranjang.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': keranjang.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return JsonResponse(data, safe=False)