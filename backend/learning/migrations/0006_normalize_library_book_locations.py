from django.db import migrations


NORMALIZED_OFFICE_LOCATION = "708 Office"
NORMALIZED_SHELF_AREA = "White Book Shelf at Reception"


def normalize_library_book_locations(apps, schema_editor):
    Book = apps.get_model("learning", "Book")
    Book.objects.filter(
        office_location="708 Office",
        shelf_area="white book shelf reception",
    ).update(shelf_area=NORMALIZED_SHELF_AREA)
    Book.objects.filter(
        office_location="BKC Office",
        shelf_area="Suman Cabin",
    ).update(
        office_location=NORMALIZED_OFFICE_LOCATION,
        shelf_area=NORMALIZED_SHELF_AREA,
        shelf_label="",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0005_booklike"),
    ]

    operations = [
        migrations.RunPython(normalize_library_book_locations, migrations.RunPython.noop),
    ]
