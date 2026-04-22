from django.urls import path

from .views import books_collection, requisition_detail, requisitions_collection, toggle_book_like

urlpatterns = [
    path("books/", books_collection, name="learning-books"),
    path("books/<int:book_id>/likes/toggle/", toggle_book_like, name="learning-book-like-toggle"),
    path("requisitions/", requisitions_collection, name="learning-requisitions"),
    path("requisitions/<int:requisition_id>/", requisition_detail, name="learning-requisition-detail"),
]
