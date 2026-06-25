from django.db import migrations


NEW_ITEM = {
    "name": "Vacuum Insulated Coffeemate Stainless Steel Travel Mug",
    "category": "drinkware",
    "description": "Vacuum insulated stainless steel travel mug for daily commute and meetings.",
    "point_cost": 50000,
    "stock_units": 10,
    "accent_hex": "#6b4a2f",
    "is_active": True,
}

UPDATED_STOCK_COUNTS = {
    "Acuite Coffee Mug": 20,
}


def update_brand_store_catalog(apps, schema_editor):
    BrandStoreItem = apps.get_model("store", "BrandStoreItem")

    for item_name, stock_units in UPDATED_STOCK_COUNTS.items():
        BrandStoreItem.objects.filter(name=item_name).update(stock_units=stock_units)

    BrandStoreItem.objects.update_or_create(
        name=NEW_ITEM["name"],
        defaults=NEW_ITEM,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0007_update_store_open_redemption_constraint"),
    ]

    operations = [
        migrations.RunPython(update_brand_store_catalog, migrations.RunPython.noop),
    ]
