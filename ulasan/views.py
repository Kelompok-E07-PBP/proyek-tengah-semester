from django.shortcuts import render, redirect   # Tambahkan import redirect di baris ini
from ulasan.forms import UlasanEntryForm
from ulasan.models import UlasanEntry
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse

@login_required(login_url='/login')
def show_ulasan_main(request):
    ulasan_entries = UlasanEntry.objects.all()

    context = {
        'nama_halaman' : 'Ulasan',
        'ulasan_entries': ulasan_entries,
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

def show_json(request):
    data = UlasanEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

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