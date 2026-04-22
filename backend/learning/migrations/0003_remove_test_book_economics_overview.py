from django.db import migrations


def remove_test_book(apps, schema_editor):
    Book = apps.get_model("learning", "Book")
    Book.objects.filter(
        title="Economics - Overview",
        author="MR. XYZ TEST",
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0002_book_catalog_fields_and_seed"),
    ]

    operations = [
        migrations.RunPython(remove_test_book, migrations.RunPython.noop),
    ]
