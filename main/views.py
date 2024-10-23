import datetime
from django.http import HttpResponse, HttpResponseForbidden
from django.core import serializers
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.models import Product


@login_required(login_url='/login')
def show_main(request):
    cookie = request.COOKIES.get('last_login')

    if cookie:
        last_login = datetime.datetime.strptime(cookie, "%Y-%m-%d %H:%M:%S.%f")
    else:
        return redirect('main:login')

    if(request.user.is_superuser):
        return redirect('edit:show_edit_main')

    product_entries = Product.objects.all()
    context = {
        'nama_aplikasi': 'Mujur Reborn',
        'last_login': last_login,
        'product_entries': product_entries,
    }

    return render(request, "main.html", context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def login_user(request):
   if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

