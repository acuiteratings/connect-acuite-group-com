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
    path("api/battleship/", include("battleship.urls")),
    path("api/feed/", include("feed.urls")),
    path("api/learning/", include("learning.urls")),
    path("api/recognition/", include("recognition.urls")),
    path("api/store/", include("store.urls")),
    path("api/voice/", include("voice.urls")),
    path("api/directory/", include("directory.urls")),
    path("api/ops/", include("operations.urls")),
    path("api/quiz/", include("quiz.urls")),
    path("", views.home, name="home"),
    path("index.html", views.home, name="home-html"),
    path("admin-console.html", views.admin_console_page, name="admin-console-page"),
    path("access-denied.html", views.access_denied_page, name="access-denied-page"),
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
