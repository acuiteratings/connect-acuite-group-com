from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BrandStoreItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160)),
                ("category", models.CharField(choices=[("apparel", "Apparel"), ("drinkware", "Drinkware"), ("desk", "Desk"), ("memorabilia", "Memorabilia")], max_length=24)),
                ("description", models.TextField(blank=True)),
                ("point_cost", models.PositiveIntegerField(default=0)),
                ("stock_units", models.PositiveIntegerField(default=0)),
                ("accent_hex", models.CharField(blank=True, max_length=16)),
                ("image_url", models.URLField(blank=True, max_length=500)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ("category", "point_cost", "name"),
            },
        ),
        migrations.CreateModel(
            name="BrandStoreRedemption",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("requested", "Requested"), ("approved", "Approved"), ("fulfilled", "Fulfilled"), ("declined", "Declined"), ("cancelled", "Cancelled")], default="requested", max_length=16)),
                ("points_locked", models.PositiveIntegerField()),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("item", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="redemptions", to="store.brandstoreitem")),
                ("requester", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="brand_store_redemptions", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ("-created_at",),
            },
        ),
    ]
