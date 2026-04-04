from django.conf import settings
from django.db import models


class BrandStoreItem(models.Model):
    class Category(models.TextChoices):
        APPAREL = "apparel", "Apparel"
        DRINKWARE = "drinkware", "Drinkware"
        DESK = "desk", "Desk"
        MEMORABILIA = "memorabilia", "Memorabilia"

    name = models.CharField(max_length=160)
    category = models.CharField(max_length=24, choices=Category.choices)
    description = models.TextField(blank=True)
    point_cost = models.PositiveIntegerField(default=0)
    stock_units = models.PositiveIntegerField(default=0)
    accent_hex = models.CharField(max_length=16, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("category", "point_cost", "name")

    def __str__(self):
        return self.name


class BrandStoreRedemption(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        APPROVED = "approved", "Approved"
        FULFILLED = "fulfilled", "Fulfilled"
        DECLINED = "declined", "Declined"
        CANCELLED = "cancelled", "Cancelled"

    item = models.ForeignKey(BrandStoreItem, on_delete=models.CASCADE, related_name="redemptions")
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="brand_store_redemptions",
    )
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.REQUESTED)
    points_locked = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    admin_note = models.CharField(max_length=280, blank=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("item", "requester"),
                condition=models.Q(status__in=("requested", "approved", "fulfilled")),
                name="store_unique_open_redemption_per_item_requester",
            )
        ]

    def __str__(self):
        return f"{self.requester.full_name} -> {self.item.name}"


class CoinLedgerEntry(models.Model):
    class EntryType(models.TextChoices):
        EARN = "earn", "Earn"
        EARN_REVERSAL = "earn_reversal", "Earn reversal"
        HOLD = "hold", "Hold"
        RELEASE = "release", "Release"
        SPEND = "spend", "Spend"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="coin_ledger_entries",
    )
    entry_type = models.CharField(max_length=24, choices=EntryType.choices)
    event_key = models.CharField(max_length=64)
    amount = models.PositiveIntegerField()
    reference_key = models.CharField(max_length=180, unique=True)
    summary = models.CharField(max_length=280, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    occurred_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-occurred_at", "-id")
        indexes = [
            models.Index(fields=("user", "occurred_at")),
            models.Index(fields=("user", "entry_type")),
        ]

    def __str__(self):
        return f"{self.user.full_name} | {self.entry_type} | {self.amount}"
