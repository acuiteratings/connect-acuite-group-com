from django.db import migrations
from django.db.models import Q


def remove_test_book_variants(apps, schema_editor):
    Book = apps.get_model("learning", "Book")
    Book.objects.filter(
        Q(title__icontains="economics - overview")
        & Q(author__icontains="xyz test")
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0003_remove_test_book_economics_overview"),
    ]

    operations = [
        migrations.RunPython(remove_test_book_variants, migrations.RunPython.noop),
    ]
