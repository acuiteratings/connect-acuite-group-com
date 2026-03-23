from django.http import HttpResponse
from django.urls import path


def boom_view(request):
    raise RuntimeError("Synthetic middleware failure")


urlpatterns = [
    path("boom/", boom_view),
]
