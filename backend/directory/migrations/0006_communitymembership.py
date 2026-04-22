from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone


COMMUNITY_CLUB_KEYS = {
    "reading_club",
    "movie_club",
    "travel_club",
    "entertainment_club",
    "quiz_club",
    "debate_club",
    "technology_club",
    "photography_club",
    "cricket_club",
    "football_club",
    "charity_club",
    "health_club",
}


def _normalize_clubs(value):
    cleaned = []
    seen = set()
    for item in value if isinstance(value, (list, tuple)) else []:
        club_key = str(item or "").strip().lower()
        if not club_key or club_key in seen or club_key not in COMMUNITY_CLUB_KEYS:
            continue
        seen.add(club_key)
        cleaned.append(club_key)
    return cleaned


def backfill_community_memberships(apps, schema_editor):
    DirectoryProfile = apps.get_model("directory", "DirectoryProfile")
    CommunityMembership = apps.get_model("directory", "CommunityMembership")

    profiles = DirectoryProfile.objects.select_related("user").order_by("created_at", "id")
    seen_memberships = set()

    for profile in profiles.iterator():
        joined_at = profile.created_at or timezone.now()
        for club_key in _normalize_clubs(profile.clubs):
            membership_key = (profile.user_id, club_key)
            if membership_key in seen_memberships:
                continue
            CommunityMembership.objects.create(
                user_id=profile.user_id,
                club_key=club_key,
                is_admin=False,
                joined_at=joined_at,
            )
            seen_memberships.add(membership_key)

    for club_key in COMMUNITY_CLUB_KEYS:
        first_membership = CommunityMembership.objects.filter(club_key=club_key).order_by("joined_at", "id").first()
        if first_membership and not first_membership.is_admin:
            first_membership.is_admin = True
            first_membership.save(update_fields=["is_admin", "updated_at"])


def reverse_backfill_community_memberships(apps, schema_editor):
    CommunityMembership = apps.get_model("directory", "CommunityMembership")
    CommunityMembership.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("directory", "0005_directoryprofile_clubs"),
    ]

    operations = [
        migrations.CreateModel(
            name="CommunityMembership",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("club_key", models.CharField(max_length=64)),
                ("is_admin", models.BooleanField(default=False)),
                ("joined_at", models.DateTimeField(default=timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="community_memberships", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ("club_key", "joined_at", "id"),
            },
        ),
        migrations.AddConstraint(
            model_name="communitymembership",
            constraint=models.UniqueConstraint(fields=("user", "club_key"), name="directory_unique_membership_per_user_club"),
        ),
        migrations.RunPython(
            backfill_community_memberships,
            reverse_backfill_community_memberships,
        ),
    ]
