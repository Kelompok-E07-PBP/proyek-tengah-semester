# pengiriman/views.py
import json
from django.shortcuts import render, redirect
from pengiriman.models import Pengiriman
from pengiriman.forms import PengirimanForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from keranjang.models import Keranjang
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required(login_url='/login')
def pengiriman_view(request):
    keranjang_id = request.GET.get('keranjang_id')

    if keranjang_id:
        try:
            keranjang = Keranjang.objects.get(id=keranjang_id, user=request.user)
            items = keranjang.itemkeranjang_set.all()
        except Keranjang.DoesNotExist:
            items = None
    else:
        items = None

    if request.method == 'POST':
        form = PengirimanForm(request.POST)
        if form.is_valid():
            pengiriman = form.save(commit=False)
            pengiriman.user = request.user
            pengiriman.save()
            return redirect(f"{reverse('pembayaran:pembayaran_view')}?keranjang_id={keranjang_id}")
        else:
            form = PengirimanForm(request.POST)
    else:
        form = PengirimanForm()

    return render(request, 'pengiriman.html', {
        'form': form,
        'items': items,
        'keranjang': keranjang if items else None
    })

@login_required(login_url='/login')
@csrf_exempt
def process_pengiriman_ajax(request):
    if request.method == "POST":
        user = request.user
        try:
            keranjang = Keranjang.objects.get(user=user)
        except Keranjang.DoesNotExist:
            return JsonResponse({'error': 'Keranjang tidak ditemukan.'}, status=404)

        if not keranjang.itemkeranjang_set.exists():
            return JsonResponse({'error': 'Keranjang kosong, tidak dapat melakukan pengiriman.'}, status=400)

        form_data = request.POST
        pengiriman = Pengiriman(
            user=user,
            first_name=form_data.get('first_name'),
            last_name=form_data.get('last_name'),
            email=form_data.get('email'),
            phone_number=form_data.get('phone_number'),
            address=form_data.get('address'),
            city=form_data.get('city'),
            postal_code=form_data.get('postal_code'),
            courier=form_data.get('courier')
        )

        try:
            pengiriman.save()
            return JsonResponse({'message': 'Pengiriman berhasil dibuat!', 'pengiriman_id': pengiriman.id})
        except Exception as e:
            print("Error during pengiriman processing:", e)
            return JsonResponse({'error': 'Terjadi kesalahan saat melakukan pengiriman.'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required(login_url='/login')
def show_json(request):
    try:
        data = Pengiriman.objects.all()
        return HttpResponse(serializers.serialize("json", data), content_type="application/json")
    except Exception as e:
        print("Error fetching data:", e)
        return JsonResponse({'error': 'Terjadi kesalahan dalam mengambil data.'}, status=500)
