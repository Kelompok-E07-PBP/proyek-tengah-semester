from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import Pembayaran
from .forms import PembayaranForm
from pengiriman.models import Pengiriman
from keranjang.models import Keranjang
from django.contrib.auth.decorators import login_required
from django.core import serializers

@login_required(login_url='/login')
def pembayaran_view(request):
    user = request.user

    keranjang = Keranjang.objects.get_or_create(user=user)[0]
    form = PembayaranForm(request.POST or None)
    total_harga_keranjang = keranjang.get_total()

    try:
        pengiriman = Pengiriman.objects.filter(user=user).latest('created_at')
        city = pengiriman.city
        delivery_fee = calculate_delivery_fee(city)
    except Pengiriman.DoesNotExist:
        pengiriman = None
        delivery_fee = 0

    total_harga = total_harga_keranjang + delivery_fee

    if form.is_valid() and request.method == "POST":
        if not keranjang.itemkeranjang_set.exists() or not pengiriman:
            return HttpResponse('Keranjang kosong atau informasi pengiriman tidak lengkap.', status=400)

        selected_payment_method = request.POST.get('payment_method')
        if not selected_payment_method:
            return HttpResponse('Please select a payment method', status=400)

        pembayaran = form.save(commit=False)
        pembayaran.user = user
        pembayaran.amount = total_harga
        pembayaran.payment_method = selected_payment_method
        pembayaran.save()

        keranjang.itemkeranjang_set.all().delete()

        return redirect("main:show_main")

    context = {
        'form': form,
        'keranjang_items': keranjang.itemkeranjang_set.all(),
        'pengiriman': pengiriman,
        'delivery_fee': delivery_fee,
        'total_harga': total_harga,
    }
    return render(request, 'pembayaran.html', context)

@login_required(login_url='/login')
def process_payment_ajax(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user = request.user
        keranjang = get_object_or_404(Keranjang, user=user)

        if not keranjang.itemkeranjang_set.exists():
            return JsonResponse({'error': 'Keranjang kosong, tidak dapat melakukan pembayaran.'}, status=400)

        total_harga_keranjang = keranjang.get_total()
        payment_method = request.POST.get('payment_method')
        if not payment_method:
            return JsonResponse({'error': 'Please select a payment method.'}, status=400)

        try:
            pengiriman = Pengiriman.objects.get(user=user)
            city = pengiriman.city
            delivery_fee = calculate_delivery_fee(city)
        except Pengiriman.DoesNotExist:
            return JsonResponse({'error': 'Informasi pengiriman tidak lengkap.'}, status=400)

        total_harga = total_harga_keranjang + delivery_fee

        try:
            pembayaran = Pembayaran.objects.create(
                user=user,
                amount=total_harga,
                payment_method=payment_method
            )
            pembayaran.save()

            keranjang.itemkeranjang_set.all().delete()

            return JsonResponse({'message': 'Payment successful!', 'total_amount': total_harga})
        except Exception as e:
            print("Error during payment processing:", e)
            return JsonResponse({'error': 'Terjadi kesalahan saat melakukan pembayaran.'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def calculate_delivery_fee(city):
    fees = {
        'Jakarta Barat': 10000,
        'Jakarta Pusat': 12000,
        'Jakarta Selatan': 15000,
        'Jakarta Timur': 13000,
        'Jakarta Utara': 11000,
    }
    return fees.get(city, 20000)

@login_required(login_url='/login')
def show_json(request):
    user = request.user
    data = Pembayaran.objects.filter(user=user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
