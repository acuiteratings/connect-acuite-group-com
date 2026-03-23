from django.urls import path

from .views import directory_list

urlpatterns = [
    path("", directory_list, name="directory-list"),
]
