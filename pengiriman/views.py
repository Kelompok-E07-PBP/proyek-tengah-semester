# pengiriman/views.py
from django.shortcuts import render, redirect, get_object_or_404
from pengiriman.models import Pengiriman
from pengiriman.forms import PengirimanForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from keranjang.models import Keranjang
from django.urls import reverse

@login_required(login_url='/login')
def pengiriman_view(request):
    keranjang_id = request.GET.get('keranjang_id')
    keranjang = get_object_or_404(Keranjang, id=keranjang_id, user=request.user)
    items = keranjang.itemkeranjang_set.all()

    if request.method == 'POST':
        form = PengirimanForm(request.POST)
        if form.is_valid():
            pengiriman = form.save(commit=False)
            pengiriman.user = request.user
            pengiriman.save()
            return redirect(f"{reverse('pembayaran:pembayaran_view')}?keranjang_id={keranjang_id}")

    else:
        form = PengirimanForm()

    return render(request, 'pengiriman.html', {'form': form, 'items': items, 'keranjang': keranjang})

def show_json(request):
    data = Pengiriman.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

