from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def home(request):
    return render(request, "index.html", {"api_base_path": "/api"})


@ensure_csrf_cookie
def login_page(request):
    return render(request, "login.html", {"api_base_path": "/api"})
