from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Pembayaran, PaymentMethod
from .forms import PembayaranForm
from main.models import Product
from pengiriman.models import Pengiriman
from keranjang.models import Keranjang
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.urls import reverse

@login_required(login_url='/login')
def pembayaran_view(request):
    user = request.user
    form = PembayaranForm(request.POST or None)

    keranjang = get_object_or_404(Keranjang, user=user)
    total_harga_keranjang = keranjang.get_total()

    pengiriman = get_object_or_404(Pengiriman, user=user)
    city = pengiriman.city
    delivery_fee = calculate_delivery_fee(city) 

    total_harga = total_harga_keranjang + delivery_fee

    payment_methods = PaymentMethod.objects.filter(user=user)

    if form.is_valid() and request.method == "POST":
        selected_payment_method = request.POST.get('payment_methods')
        if not selected_payment_method:
            return HttpResponse('Please select payment method', status=400)
        
        pembayaran = form.save(commit=False)
        pembayaran.user = request.user 
        pembayaran.amount = total_harga
        pembayaran.payment_method = get_object_or_404(PaymentMethod, id=selected_payment_method, user=user)
        pembayaran.save()
        return redirect("main:show_main")

    context = {
        'form': form,
        'keranjang_items': keranjang.itemkeranjang_set.all(),
        'delivery_fee': delivery_fee,
        'total_harga': total_harga,
        'payment_methods': payment_methods,
    }
    return render(request, 'pembayaran.html', context)

def calculate_delivery_fee(city):
    if city == 'Jakarta Barat':
        return 10000
    elif city == 'Jakarta Pusat':
        return 12000
    elif city == 'Jakarta Selatan':
        return 15000
    elif city == 'Jakarta Timur':
        return 13000
    elif city == 'Jakarta Utara':
        return 11000
    else:
        return 20000  

@login_required(login_url='/login')
def show_json(request):
    user = request.user
    data = Pembayaran.objects.filter(user=user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
