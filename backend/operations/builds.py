import os

from django.conf import settings
from django.db import OperationalError, ProgrammingError, transaction

from .models import BuildState

BUILD_PREFIX = "1.000000"
BUILD_STATE_KEY = "primary"


def format_build_number(counter):
    safe_counter = max(int(counter or 1), 1)
    return f"{BUILD_PREFIX}{safe_counter}"


def parse_build_counter(build_number):
    value = str(build_number or "").strip()
    if value.startswith(BUILD_PREFIX):
        suffix = value[len(BUILD_PREFIX) :]
        if suffix.isdigit():
            return max(int(suffix), 1)
    digits = "".join(character for character in value if character.isdigit())
    if digits:
        return max(int(digits[-1]), 1)
    return 1


def get_seed_counter():
    seed_value = os.getenv("APP_BUILD_COUNTER_SEED", "").strip()
    if seed_value.isdigit():
        return max(int(seed_value), 1)
    return parse_build_counter(getattr(settings, "APP_BUILD_NUMBER", "1.0000001"))


def get_current_build_number():
    try:
        state = BuildState.objects.only("display_number").filter(
            singleton_key=BUILD_STATE_KEY
        ).first()
    except (OperationalError, ProgrammingError):
        return settings.APP_BUILD_NUMBER
    if state and state.display_number:
        return state.display_number
    return settings.APP_BUILD_NUMBER


def register_build_deploy(commit_sha=""):
    seed_counter = get_seed_counter()
    with transaction.atomic():
        state, _created = BuildState.objects.select_for_update().get_or_create(
            singleton_key=BUILD_STATE_KEY,
            defaults={
                "counter": seed_counter,
                "display_number": format_build_number(seed_counter),
                "commit_sha": str(commit_sha or "")[:64],
            },
        )
        current_counter = max(state.counter or 0, seed_counter)
        state.counter = current_counter + 1
        state.display_number = format_build_number(state.counter)
        state.commit_sha = str(commit_sha or os.getenv("RENDER_GIT_COMMIT", "")).strip()[:64]
        state.save(
            update_fields=[
                "counter",
                "display_number",
                "commit_sha",
                "updated_at",
            ]
        )
    return state
