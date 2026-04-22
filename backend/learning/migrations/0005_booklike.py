from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0004_remove_variants_of_test_book"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BookLike",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("book", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="likes", to="learning.book")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="liked_books", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-created_at",)},
        ),
        migrations.AddConstraint(
            model_name="booklike",
            constraint=models.UniqueConstraint(fields=("book", "user"), name="learning_unique_book_like"),
        ),
    ]
