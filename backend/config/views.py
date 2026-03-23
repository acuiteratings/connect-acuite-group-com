from django.shortcuts import render


def home(request):
    return render(request, "index.html", {"api_base_path": "/api"})


def login_page(request):
    return render(request, "login.html", {"api_base_path": "/api"})
