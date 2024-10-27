from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Ulasan
from .forms import UlasanForm

def ulasan_app(request):
    ulasans = Ulasan.objects.all()  # Ambil semua ulasan dari database
    return render(request, 'ulasan_app/ulasan_app.html', {'ulasans': ulasans})

def create_ulasan(request):
    if request.method == 'POST':
        form = UlasanForm(request.POST)
        if form.is_valid():
            ulasan = form.save(commit=False)
            ulasan.user = request.user  # Set user saat ini
            ulasan.save()
            return redirect('ulasan_app')  # Kembali ke halaman ulasan setelah membuat
    else:
        form = UlasanForm()
    return render(request, 'ulasan_app/create_ulasan_app.html', {'form': form})

def hapus_ulasan(request, ulasan_id):
    ulasan = get_object_or_404(Ulasan, id=ulasan_id)
    if request.method == 'POST':
        ulasan.delete()
        return redirect('ulasan_app')  # Kembali ke halaman ulasan setelah menghapus
    return render(request, 'ulasan_app/delete_ulasan_app.html', {'ulasan': ulasan})

def show_json(request):
    ulasans = list(Ulasan.objects.values())
    return JsonResponse(ulasans, safe=False)

def show_json_ajax(request):
    if request.is_ajax():
        ulasans = list(Ulasan.objects.values())
        return JsonResponse(ulasans, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)