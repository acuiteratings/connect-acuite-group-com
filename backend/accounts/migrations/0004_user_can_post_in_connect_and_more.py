from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_trustedapplogingrant"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "ordering": ("email",),
                "permissions": [
                    ("manage_access_rights", "Can assign Connect access rights"),
                    ("post_as_company", "Can post on behalf of the company"),
                    ("disable_connect_posting", "Can disable posting access in Connect"),
                ],
            },
        ),
        migrations.AddField(
            model_name="user",
            name="can_post_in_connect",
            field=models.BooleanField(default=True),
        ),
    ]
