from django.contrib import admin

from .models import BattleshipEvent, BattleshipMatch, BattleshipParticipant, BattleshipShot


class BattleshipParticipantInline(admin.TabularInline):
    model = BattleshipParticipant
    extra = 0


@admin.register(BattleshipMatch)
class BattleshipMatchAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "inviter",
        "invitee",
        "status",
        "occupies_global_slot",
        "turn_owner",
        "winner",
        "created_at",
    )
    list_filter = ("status", "occupies_global_slot")
    search_fields = ("inviter__email", "invitee__email", "inviter__display_name", "invitee__display_name")
    inlines = [BattleshipParticipantInline]


@admin.register(BattleshipShot)
class BattleshipShotAdmin(admin.ModelAdmin):
    list_display = ("match", "turn_number", "shooter", "target_participant", "row", "col", "result", "created_at")
    list_filter = ("result",)
    search_fields = ("match__id", "shooter__email")


@admin.register(BattleshipEvent)
class BattleshipEventAdmin(admin.ModelAdmin):
    list_display = ("match", "event_type", "actor", "summary", "created_at")
    list_filter = ("event_type",)
    search_fields = ("summary", "actor__email")
