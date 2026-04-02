from django.urls import path

from .views import books_collection, requisition_detail, requisitions_collection

urlpatterns = [
    path("books/", books_collection, name="learning-books"),
    path("requisitions/", requisitions_collection, name="learning-requisitions"),
    path("requisitions/<int:requisition_id>/", requisition_detail, name="learning-requisition-detail"),
]
