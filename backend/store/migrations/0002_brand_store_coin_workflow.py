from django.db import migrations, models


def seed_brand_store_items(apps, schema_editor):
    BrandStoreItem = apps.get_model("store", "BrandStoreItem")

    items = [
        {
            "name": "Acuite Coffee Mug",
            "category": "drinkware",
            "description": "Ceramic Acuite mug for desk and meeting-room use.",
            "point_cost": 30000,
            "stock_units": 24,
            "accent_hex": "#8c5a33",
        },
        {
            "name": "Acuite T Shirt",
            "category": "apparel",
            "description": "Branded Acuite crew-neck t-shirt for employee events.",
            "point_cost": 100000,
            "stock_units": 20,
            "accent_hex": "#28375a",
        },
        {
            "name": "Acuite Cricket Bat",
            "category": "memorabilia",
            "description": "Signature Acuite cricket bat for office tournaments and gifting.",
            "point_cost": 250000,
            "stock_units": 6,
            "accent_hex": "#7c4d18",
        },
        {
            "name": "Acuite Laptop Bag",
            "category": "apparel",
            "description": "Branded laptop bag for daily office commute.",
            "point_cost": 180000,
            "stock_units": 15,
            "accent_hex": "#3a4d5f",
        },
        {
            "name": "Acuite Necktie",
            "category": "apparel",
            "description": "Formal Acuite necktie for client meetings and formal days.",
            "point_cost": 45000,
            "stock_units": 18,
            "accent_hex": "#5a2436",
        },
        {
            "name": "Acuite Pen",
            "category": "desk",
            "description": "Executive Acuite pen for notebooks, meetings and signatures.",
            "point_cost": 10000,
            "stock_units": 40,
            "accent_hex": "#325b5b",
        },
    ]

    for item in items:
        BrandStoreItem.objects.update_or_create(
            name=item["name"],
            defaults=item,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="brandstoreredemption",
            name="admin_note",
            field=models.CharField(blank=True, max_length=280),
        ),
        migrations.AddField(
            model_name="brandstoreredemption",
            name="reviewed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddConstraint(
            model_name="brandstoreredemption",
            constraint=models.UniqueConstraint(
                condition=models.Q(status__in=("requested", "approved", "fulfilled")),
                fields=("item", "requester"),
                name="store_unique_open_redemption_per_item_requester",
            ),
        ),
        migrations.RunPython(seed_brand_store_items, migrations.RunPython.noop),
    ]
