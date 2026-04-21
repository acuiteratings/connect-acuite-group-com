from django.urls import path

from .views import communities_overview, directory_list, my_profile

urlpatterns = [
    path("", directory_list, name="directory-list"),
    path("communities/", communities_overview, name="directory-communities"),
    path("me/", my_profile, name="directory-my-profile"),
]
