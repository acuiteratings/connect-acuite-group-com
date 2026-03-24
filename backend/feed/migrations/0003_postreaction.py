from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feed", "0002_post_module_topic_metadata"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PostReaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reaction_type", models.CharField(choices=[("like", "Like")], default="like", max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("post", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="reactions", to="feed.post")),
                ("user", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="post_reactions", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ("-updated_at",),
            },
        ),
        migrations.AddConstraint(
            model_name="postreaction",
            constraint=models.UniqueConstraint(fields=("post", "user", "reaction_type"), name="feed_unique_reaction_per_post_user_type"),
        ),
    ]
