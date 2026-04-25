from django.db import migrations


QUESTION = "Which training would you want us to organise for you next?"
DESCRIPTION = "Select one option below. The vote count is shown next to each training."
OPTIONS = [
    "Selling Credit Rating",
    "Using AI for better work life balance",
    "Leading a high performance team",
    "Data analytics for rating analysts",
    "Create and manage personal wealth",
]


def create_training_poll(apps, schema_editor):
    Poll = apps.get_model("voice", "Poll")
    PollOption = apps.get_model("voice", "PollOption")

    Poll.objects.filter(is_active=True).update(is_active=False)

    poll, _ = Poll.objects.get_or_create(
        question=QUESTION,
        defaults={
            "description": DESCRIPTION,
            "is_active": True,
        },
    )
    poll.description = DESCRIPTION
    poll.is_active = True
    poll.save(update_fields=["description", "is_active", "updated_at"])

    PollOption.objects.filter(poll=poll).exclude(label__in=OPTIONS).delete()
    existing_labels = set(PollOption.objects.filter(poll=poll).values_list("label", flat=True))
    for position, label in enumerate(OPTIONS, start=1):
        if label in existing_labels:
            PollOption.objects.filter(poll=poll, label=label).update(position=position)
        else:
            PollOption.objects.create(
                poll=poll,
                label=label,
                position=position,
            )


class Migration(migrations.Migration):
    dependencies = [
        ("voice", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_training_poll,
            migrations.RunPython.noop,
        ),
    ]
