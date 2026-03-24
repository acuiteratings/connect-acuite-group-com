from django.core.management.base import BaseCommand, CommandError

from accounts.models import User


class Command(BaseCommand):
    help = "Set Acuite Connect access level and posting privileges for one or more users."

    def add_arguments(self, parser):
        parser.add_argument(
            "emails",
            nargs="+",
            help="One or more employee email addresses to update.",
        )
        parser.add_argument(
            "--access-level",
            default=User.AccessLevel.EMPLOYEE,
            choices=[
                User.AccessLevel.EMPLOYEE,
                User.AccessLevel.MODERATOR,
                User.AccessLevel.ADMIN,
            ],
            help="Connect access level to assign.",
        )
        parser.add_argument(
            "--enable-posting",
            action="store_true",
            help="Explicitly enable posting in Connect for the selected users.",
        )
        parser.add_argument(
            "--disable-posting",
            action="store_true",
            help="Explicitly disable posting in Connect for the selected users.",
        )

    def handle(self, *args, **options):
        emails = [str(email or "").strip().lower() for email in options["emails"] if str(email or "").strip()]
        access_level = options["access_level"]
        enable_posting = bool(options["enable_posting"])
        disable_posting = bool(options["disable_posting"])

        if not emails:
            raise CommandError("At least one email address is required.")
        if enable_posting and disable_posting:
            raise CommandError("Choose either --enable-posting or --disable-posting, not both.")

        updated = []
        for email in emails:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist as exc:
                raise CommandError(f"No employee account found for {email}.") from exc

            user.access_level = access_level
            if enable_posting:
                user.can_post_in_connect = True
            elif disable_posting:
                user.can_post_in_connect = False
            user.save(update_fields=["access_level", "can_post_in_connect", "updated_at"])
            updated.append(
                f"{user.email} -> {user.access_level} (posting={'enabled' if user.can_post_in_connect else 'disabled'})"
            )

        self.stdout.write(self.style.SUCCESS("Updated Connect access:"))
        for line in updated:
            self.stdout.write(f" - {line}")
