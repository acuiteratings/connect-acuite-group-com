from django.urls import path

from .views import recognition_overview

urlpatterns = [
    path("overview/", recognition_overview, name="recognition-overview"),
]
