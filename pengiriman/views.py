# pengiriman/views.py
from django.shortcuts import render, redirect
from pengiriman.models import Pengiriman
from pengiriman.forms import PengirimanForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse

@login_required(login_url='/login')
def pengiriman_view(request):  
    if request.method == 'POST':
        form = PengirimanForm(request.POST)
        if form.is_valid():
            pengiriman = form.save(commit=False)
            pengiriman.user = request.user
            pengiriman.save()
            return redirect('pembayaran:pembayaran_view')
    else:
        form = PengirimanForm()
    
    return render(request, 'pengiriman.html', {'form': form})  

def show_json(request):
    data = Pengiriman.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

