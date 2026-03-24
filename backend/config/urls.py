from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.views.static import serve

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/feed/", include("feed.urls")),
    path("api/learning/", include("learning.urls")),
    path("api/directory/", include("directory.urls")),
    path("api/ops/", include("operations.urls")),
    path("", views.home, name="home"),
    path("index.html", views.home, name="home-html"),
    path("login.html", views.login_page, name="login-page"),
    path(
        "login/",
        RedirectView.as_view(pattern_name="login-page", permanent=False),
        name="login",
    ),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^assets/(?P<path>.*)$",
            serve,
            {"document_root": Path(settings.FRONTEND_ASSET_ROOT)},
        )
    ]
