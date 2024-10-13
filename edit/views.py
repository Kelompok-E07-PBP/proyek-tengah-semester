from django.shortcuts import render

def show_main(request):
    context = {
        'nama_aplikasi': 'Mujur Reborn Admin',
    }

    return render(request, "main.html", context)
