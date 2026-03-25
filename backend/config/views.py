from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from operations.builds import get_current_build_number


@ensure_csrf_cookie
def home(request):
    return render(
        request,
        "index.html",
        {
            "api_base_path": "/api",
            "build_number": get_current_build_number(),
            "build_credit": settings.APP_BUILD_CREDIT,
        },
    )


@ensure_csrf_cookie
def login_page(request):
    return render(
        request,
        "login.html",
        {
            "api_base_path": "/api",
            "build_number": get_current_build_number(),
            "build_credit": settings.APP_BUILD_CREDIT,
        },
    )


@ensure_csrf_cookie
def admin_console_page(request):
    if not request.user.is_authenticated:
        return redirect("/login.html?next=/admin-console.html")
    if not getattr(request.user, "can_administer_connect", False):
        return redirect("/")

    return render(
        request,
        "admin-console.html",
        {
            "api_base_path": "/api",
            "build_number": get_current_build_number(),
            "build_credit": settings.APP_BUILD_CREDIT,
        },
    )
