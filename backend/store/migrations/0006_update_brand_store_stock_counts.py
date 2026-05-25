from django.db import migrations


STOCK_COUNTS = {
    "Acuite T Shirt": 100,
    "Acuite Coffee Mug": 50,
    "Acuite Laptop Bag": 30,
    "Acuite Cricket Bat": 15,
}


def update_stock_counts(apps, schema_editor):
    BrandStoreItem = apps.get_model("store", "BrandStoreItem")
    for item_name, stock_units in STOCK_COUNTS.items():
        BrandStoreItem.objects.filter(name=item_name).update(stock_units=stock_units)


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0005_update_tshirt_price"),
    ]

    operations = [
        migrations.RunPython(update_stock_counts, migrations.RunPython.noop),
    ]
