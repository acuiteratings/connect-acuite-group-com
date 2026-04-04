from django.contrib import admin

from .models import BrandStoreItem, BrandStoreRedemption, CoinLedgerEntry


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


@admin.register(CoinLedgerEntry)
class CoinLedgerEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "entry_type", "event_key", "amount", "occurred_at")
    list_filter = ("entry_type", "event_key", "occurred_at")
    search_fields = ("user__email", "summary", "reference_key")
    readonly_fields = (
        "user",
        "entry_type",
        "event_key",
        "amount",
        "reference_key",
        "summary",
        "metadata",
        "occurred_at",
        "created_at",
    )
