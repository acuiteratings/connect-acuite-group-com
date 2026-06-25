from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_update_brand_store_stock_counts"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="brandstoreredemption",
            name="store_unique_open_redemption_per_item_requester",
        ),
        migrations.AddConstraint(
            model_name="brandstoreredemption",
            constraint=models.UniqueConstraint(
                fields=("item", "requester"),
                condition=models.Q(("status__in", ("requested", "approved"))),
                name="store_unique_open_redemption_per_item_requester",
            ),
        ),
    ]
