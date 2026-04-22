from django.db import migrations


def update_store_item_prices(apps, schema_editor):
    BrandStoreItem = apps.get_model("store", "BrandStoreItem")

    price_updates = {
        "Acuite Coffee Mug": 5000,
        "Acuite T Shirt": 10000,
    }

    for item_name, point_cost in price_updates.items():
        BrandStoreItem.objects.filter(name=item_name).update(point_cost=point_cost)


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0003_coin_ledger_entry"),
    ]

    operations = [
        migrations.RunPython(update_store_item_prices, migrations.RunPython.noop),
    ]
