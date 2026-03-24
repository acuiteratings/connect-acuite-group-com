from django.contrib import admin

from .models import BrandStoreItem, BrandStoreRedemption


@admin.register(BrandStoreItem)
class BrandStoreItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "point_cost", "stock_units", "is_active", "updated_at")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")


@admin.register(BrandStoreRedemption)
class BrandStoreRedemptionAdmin(admin.ModelAdmin):
    list_display = ("item", "requester", "status", "points_locked", "created_at")
    list_filter = ("status", "item__category", "created_at")
    search_fields = ("item__name", "requester__email", "requester__first_name", "requester__last_name")
    autocomplete_fields = ("item", "requester")
