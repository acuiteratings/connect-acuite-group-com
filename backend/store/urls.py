from django.urls import path

from .views import redemption_collection, store_overview

urlpatterns = [
    path("overview/", store_overview, name="store-overview"),
    path("redemptions/", redemption_collection, name="store-redemptions"),
]
