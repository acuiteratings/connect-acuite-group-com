from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("feed", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="metadata",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="post",
            name="module",
            field=models.CharField(
                choices=[
                    ("general", "General"),
                    ("community", "Community Exchange"),
                    ("clubs_learning", "Clubs & Learning"),
                    ("ideas_voice", "Ideas & Voice"),
                    ("recognition", "Recognition"),
                    ("business", "Business Desk"),
                ],
                default="general",
                max_length=32,
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="topic",
            field=models.CharField(blank=True, default="", max_length=64),
        ),
    ]
