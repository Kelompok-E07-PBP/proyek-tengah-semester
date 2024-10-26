from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Pembayaran
from .forms import PembayaranForm
from pengiriman.models import Pengiriman
from keranjang.models import Keranjang
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required(login_url='/login')
def pembayaran_view(request):
    user = request.user
    form = PembayaranForm(request.POST or None)

    keranjang = get_object_or_404(Keranjang, user=user)
    total_harga_keranjang = keranjang.get_total()

    delivery_fee = 0
    if keranjang.itemkeranjang_set.exists():
        try:
            pengiriman = Pengiriman.objects.get(user=user)
            city = pengiriman.city
            delivery_fee = calculate_delivery_fee(city)
        except Pengiriman.DoesNotExist:
            delivery_fee = 0  

    total_harga = total_harga_keranjang + delivery_fee

    if form.is_valid() and request.method == "POST":
        if not keranjang.itemkeranjang_set.exists():
            return HttpResponse('Keranjang kosong, tidak dapat melakukan pembayaran.', status=400)

        selected_payment_method = request.POST.get('payment_method')
        if not selected_payment_method:
            return HttpResponse('Please select a payment method', status=400)

        pembayaran = form.save(commit=False)
        pembayaran.user = request.user
        pembayaran.amount = total_harga
        pembayaran.payment_method = selected_payment_method
        pembayaran.save()

        keranjang.itemkeranjang_set.all().delete()

        delivery_fee = 0
        total_harga = 0

        return redirect("main:show_main")

    context = {
        'form': form,
        'keranjang_items': keranjang.itemkeranjang_set.all(),
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
            delivery_fee = 0

        total_harga = total_harga_keranjang + delivery_fee

        pembayaran = Pembayaran.objects.create(
            user=user,
            amount=total_harga,
            payment_method=payment_method
        )
        pembayaran.save()

        keranjang.itemkeranjang_set.all().delete()

        delivery_fee = 0
        total_harga = 0

        return JsonResponse({'message': 'Payment successful!'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


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
