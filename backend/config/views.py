from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from operations.builds import get_current_build_number
from accounts.services import employee_sso_enabled


@ensure_csrf_cookie
def home(request):
    if request.user.is_authenticated and not getattr(request.user, "has_employee_access", False):
        return redirect("/access-denied.html")
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
    if request.user.is_authenticated:
        if getattr(request.user, "has_employee_access", False):
            return redirect("/admin-console.html" if getattr(request.user, "can_administer_connect", False) else "/")
        return redirect("/access-denied.html")
    return render(
        request,
        "login.html",
        {
            "api_base_path": "/api",
            "build_number": get_current_build_number(),
            "build_credit": settings.APP_BUILD_CREDIT,
            "employee_sso_enabled": employee_sso_enabled(),
        },
    )


@ensure_csrf_cookie
def access_denied_page(request):
    if not request.user.is_authenticated:
        return redirect("/login.html")
    if getattr(request.user, "has_employee_access", False):
        return redirect("/")

    return render(
        request,
        "access-denied.html",
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
