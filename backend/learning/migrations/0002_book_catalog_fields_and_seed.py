import json
from pathlib import Path

from django.db import migrations, models


def seed_book_catalog(apps, schema_editor):
    Book = apps.get_model("learning", "Book")
    data_path = Path(__file__).resolve().parent.parent / "data" / "book_catalog.json"
    if not data_path.exists():
        return

    items = json.loads(data_path.read_text())
    for item in items:
        catalog_number = str(item.get("catalog_number", "")).strip()
        title = str(item.get("title", "")).strip()
        author = str(item.get("author", "")).strip()
        if not title or not author:
            continue

        defaults = {
            "slug": str(item.get("slug", "")).strip(),
            "category": str(item.get("category", "")).strip(),
            "summary": str(item.get("summary", "")).strip(),
            "review_quote": str(item.get("review_quote", "")).strip(),
            "review_source": str(item.get("review_source", "")).strip(),
            "cover_url": str(item.get("cover_url", "")).strip(),
            "office_location": str(item.get("office_location", "")).strip(),
            "shelf_area": str(item.get("shelf_area", "")).strip(),
            "shelf_label": str(item.get("shelf_label", "")).strip(),
            "total_copies": int(item.get("total_copies", 1) or 1),
            "is_active": True,
        }

        if catalog_number:
            Book.objects.update_or_create(
                catalog_number=catalog_number,
                defaults={
                    "title": title,
                    "author": author,
                    **defaults,
                },
            )
        else:
            Book.objects.update_or_create(
                title=title,
                author=author,
                defaults=defaults,
            )


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="catalog_number",
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name="book",
            name="slug",
            field=models.SlugField(blank=True, max_length=90),
        ),
        migrations.AddField(
            model_name="book",
            name="category",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="book",
            name="review_quote",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="book",
            name="review_source",
            field=models.CharField(blank=True, max_length=180),
        ),
        migrations.AddField(
            model_name="book",
            name="cover_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="book",
            name="office_location",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="book",
            name="shelf_area",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="book",
            name="shelf_label",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.RunPython(seed_book_catalog, migrations.RunPython.noop),
    ]
