from django.urls import path

from .views import (
    redemption_collection,
    redemption_detail,
    store_admin_overview,
    store_item_collection,
    store_item_detail,
    store_overview,
)

urlpatterns = [
    path("overview/", store_overview, name="store-overview"),
    path("admin/overview/", store_admin_overview, name="store-admin-overview"),
    path("items/", store_item_collection, name="store-item-collection"),
    path("items/<int:item_id>/", store_item_detail, name="store-item-detail"),
    path("redemptions/", redemption_collection, name="store-redemptions"),
    path("redemptions/<int:redemption_id>/", redemption_detail, name="store-redemption-detail"),
]
