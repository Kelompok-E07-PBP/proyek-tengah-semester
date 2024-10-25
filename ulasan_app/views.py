from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ProductReview
from .forms import ReviewForm

def ulasan_list(request):
    reviews = ProductReview.objects.all().order_by('-created_at')
    return render(request, 'ulasan.html', {'reviews': reviews})

def create_ulasan(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({'status': 'success'})
            return redirect('ulasan_list')
    else:
        form = ReviewForm()
    return render(request, 'create_ulasan.html', {'form': form})