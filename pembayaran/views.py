from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Pembayaran, PaymentMethod
from .forms import PembayaranForm
from main.models import Product
from pengiriman.models import Pengiriman
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.urls import reverse

@login_required(login_url='/login')
def pembayaran_view(request, product_id):
    product = Product.objects.get(id=product_id)
    form = PembayaranForm(request.POST or None)

    try:
        pengiriman = Pengiriman.objects.get(user=request.user)
        city = pengiriman.city
        delivery_fee = calculate_delivery_fee(city) 
    except Pengiriman.DoesNotExist:
        delivery_fee = 0

    if form.is_valid() and request.method == "POST":
        pembayaran = form.save(commit=False)
        pembayaran.user = request.user  # Assign the current user
        pembayaran.amount = product.harga + delivery_fee
        pembayaran.status = 'PENDING'
        pembayaran.save()
        return redirect("main:show_main")

    context = {
        'form': form,
        'product': product,
        'delivery_fee': delivery_fee,
        'total_amount': product.harga + delivery_fee
    }
    return render(request, 'pembayaran.html', context)

# Function to calculate delivery fee based on the city
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
        return 20000  # Default fee if the city is not in the list

@login_required(login_url='/login')
def show_json(request):
    data = Pembayaran.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
