from django.shortcuts import render, redirect   # Tambahkan import redirect di baris ini
from ulasan.forms import UlasanEntryForm
from ulasan.models import UlasanEntry
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UlasanEntrySerializer
from django.utils.html import strip_tags

@login_required(login_url='/login')
def show_ulasan_main(request):
    current_username = request.user.username if request.user.is_authenticated else None
    context = {
        'current_username': current_username,
        'nama_halaman' : 'Ulasan',
    }

    return render(request, "ulasan_main.html", context)

def create_ulasan_entry(request):

    # Bagian ini akan link komentar dengan seorang user.
    if request.method == 'POST':
        form = UlasanEntryForm(request.POST)
        if form.is_valid():
            ulasan = form.save(commit=False)
            ulasan.user = request.user
            ulasan.save()
            return redirect('ulasan:show_ulasan_main')
    else:
        form = UlasanEntryForm()

    context = {'form': form}
    return render(request, 'create_ulasan_entry.html', context)

@api_view(['GET'])
def show_json(request):
    data = UlasanEntry.objects.all()
    serializer = UlasanEntrySerializer(data, many=True)
    return Response(serializer.data)

@login_required(login_url='/login')
def edit_ulasan(request, id):
    # Ambil Ulasan berdasarkan id
    ulasan = UlasanEntry.objects.get(pk = id)

    # Set ulasan entry sebagai instance dari form
    form = UlasanEntryForm(request.POST or None, instance=ulasan)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('ulasan:show_ulasan_main'))

    context = {'form': form}
    return render(request, "edit_ulasan.html", context)

def delete_ulasan(request, id):
    ulasan = UlasanEntry.objects.get(pk = id)
    ulasan.delete()
    return HttpResponseRedirect(reverse('ulasan:show_ulasan_main'))

@csrf_exempt
@require_POST
def add_ulasan_entry_ajax(request):
    user = request.user
    nama_produk_ulas = strip_tags(request.POST.get("nama_produk_ulas"))
    rating = request.POST.get("rating")
    komentar = strip_tags(request.POST.get("komentar"))
    

    new_ulasan = UlasanEntry(
        user=user, nama_produk_ulas=nama_produk_ulas,
        rating=rating, komentar=komentar
    )
    new_ulasan.save()

    return HttpResponse(b"CREATED", status=201)