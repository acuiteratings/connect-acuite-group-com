from django.db import migrations


def update_tshirt_price(apps, schema_editor):
    BrandStoreItem = apps.get_model("store", "BrandStoreItem")
    BrandStoreItem.objects.filter(name="Acuite T Shirt").update(point_cost=3000)


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0004_update_store_item_prices"),
    ]

    operations = [
        migrations.RunPython(update_tshirt_price, migrations.RunPython.noop),
    ]
