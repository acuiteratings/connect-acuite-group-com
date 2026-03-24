from django.urls import path

from .views import books_collection, requisitions_collection

urlpatterns = [
    path("books/", books_collection, name="learning-books"),
    path("requisitions/", requisitions_collection, name="learning-requisitions"),
]

