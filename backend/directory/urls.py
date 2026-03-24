from django.urls import path

from .views import directory_list, my_profile

urlpatterns = [
    path("", directory_list, name="directory-list"),
    path("me/", my_profile, name="directory-my-profile"),
]
