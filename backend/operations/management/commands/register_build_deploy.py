import os

from django.core.management.base import BaseCommand

from operations.builds import register_build_deploy


class Command(BaseCommand):
    help = "Registers a new deployed build number in the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            dest="commit_sha",
            default="",
            help="Optional commit SHA for this deploy.",
        )

    def handle(self, *args, **options):
        commit_sha = options["commit_sha"].strip() or os.getenv("RENDER_GIT_COMMIT", "").strip()
        state = register_build_deploy(commit_sha=commit_sha)
        self.stdout.write(
            self.style.SUCCESS(
                f"Registered build {state.display_number}"
                + (f" for commit {state.commit_sha}" if state.commit_sha else "")
            )
        )
