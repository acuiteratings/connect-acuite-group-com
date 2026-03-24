from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.db.models import Q


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220)),
                ("author", models.CharField(max_length=180)),
                ("summary", models.TextField(blank=True)),
                ("total_copies", models.PositiveIntegerField(default=1)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ("title", "author")},
        ),
        migrations.CreateModel(
            name="BookRequisition",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("requested", "Requested"), ("approved", "Approved"), ("issued", "Issued"), ("returned", "Returned"), ("declined", "Declined"), ("cancelled", "Cancelled")], default="requested", max_length=16)),
                ("note", models.CharField(blank=True, max_length=280)),
                ("admin_note", models.CharField(blank=True, max_length=280)),
                ("requested_at", models.DateTimeField(auto_now_add=True)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                ("issued_at", models.DateTimeField(blank=True, null=True)),
                ("returned_at", models.DateTimeField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("book", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="requisitions", to="learning.book")),
                ("requester", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="book_requisitions", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-requested_at",)},
        ),
        migrations.AddConstraint(
            model_name="bookrequisition",
            constraint=models.UniqueConstraint(
                condition=Q(status__in=("requested", "approved", "issued")),
                fields=("book", "requester"),
                name="learning_unique_open_book_requisition",
            ),
        ),
    ]
