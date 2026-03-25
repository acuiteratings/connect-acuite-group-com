from django.conf import settings
from django.db import models


class BattleshipMatch(models.Model):
    class Status(models.TextChoices):
        INVITED = "invited", "Invited"
        SHIP_PLACEMENT = "ship_placement", "Ship placement"
        ACTIVE = "active", "Active"
        PAUSED_OFFICE_HOURS = "paused_office_hours", "Paused for office hours"
        COMPLETED = "completed", "Completed"
        RESIGNED = "resigned", "Resigned"
        ABANDONED = "abandoned", "Abandoned"
        DECLINED = "declined", "Declined"
        EXPIRED = "expired", "Expired"
        CANCELLED = "cancelled", "Cancelled"

    inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="battleship_invites_sent",
    )
    invitee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="battleship_invites_received",
    )
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.INVITED)
    # We intentionally allow multiple pending invitations, but only one match may occupy the
    # serious live slot across the whole intranet. This flag is enforced with a partial unique
    # constraint so only one ship_placement / active / paused match may exist at a time.
    occupies_global_slot = models.BooleanField(default=False, db_index=True)
    paused_from_status = models.CharField(max_length=32, blank=True)
    invitation_expires_at = models.DateTimeField(blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    accepted_at = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    last_activity_at = models.DateTimeField(blank=True, null=True)
    turn_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="battleship_turns",
        blank=True,
        null=True,
    )
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="battleship_wins",
        blank=True,
        null=True,
    )
    loser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="battleship_losses",
        blank=True,
        null=True,
    )
    resigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="battleship_resignations",
        blank=True,
        null=True,
    )
    inactive_player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="battleship_inactivity_flags",
        blank=True,
        null=True,
    )
    total_turns = models.PositiveIntegerField(default=0)
    rematch_parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="rematches",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["occupies_global_slot"],
                condition=models.Q(occupies_global_slot=True),
                name="battleship_single_global_slot",
            ),
        ]

    def __str__(self):
        return f"{self.inviter} vs {self.invitee} ({self.status})"

    @classmethod
    def serious_statuses(cls):
        return [
            cls.Status.SHIP_PLACEMENT,
            cls.Status.ACTIVE,
            cls.Status.PAUSED_OFFICE_HOURS,
        ]


class BattleshipParticipant(models.Model):
    class Slot(models.TextChoices):
        CHALLENGER = "challenger", "Challenger"
        OPPONENT = "opponent", "Opponent"

    match = models.ForeignKey(
        BattleshipMatch,
        on_delete=models.CASCADE,
        related_name="participants",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="battleship_participations",
    )
    slot = models.CharField(max_length=16, choices=Slot.choices)
    fleet_layout = models.JSONField(default=list, blank=True)
    placement_ready = models.BooleanField(default=False)
    ready_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["match", "user"],
                name="battleship_unique_participant_per_match",
            ),
            models.UniqueConstraint(
                fields=["match", "slot"],
                name="battleship_unique_slot_per_match",
            ),
        ]

    def __str__(self):
        return f"{self.user} in {self.match_id}"


class BattleshipShot(models.Model):
    class Result(models.TextChoices):
        HIT = "hit", "Hit"
        MISS = "miss", "Miss"
        SUNK = "sunk", "Sunk"

    match = models.ForeignKey(
        BattleshipMatch,
        on_delete=models.CASCADE,
        related_name="shots",
    )
    shooter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="battleship_shots_fired",
    )
    target_participant = models.ForeignKey(
        BattleshipParticipant,
        on_delete=models.CASCADE,
        related_name="shots_received",
    )
    row = models.PositiveSmallIntegerField()
    col = models.PositiveSmallIntegerField()
    result = models.CharField(max_length=16, choices=Result.choices)
    ship_type = models.CharField(max_length=24, blank=True)
    turn_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("turn_number", "created_at")
        constraints = [
            models.UniqueConstraint(
                fields=["match", "turn_number"],
                name="battleship_unique_turn_number_per_match",
            ),
            models.UniqueConstraint(
                fields=["match", "target_participant", "row", "col"],
                name="battleship_unique_target_cell_per_match",
            ),
            models.CheckConstraint(
                condition=models.Q(row__gte=0, row__lt=10, col__gte=0, col__lt=10),
                name="battleship_shot_within_grid",
            ),
        ]

    def __str__(self):
        return f"{self.match_id} turn {self.turn_number} {self.result}"


class BattleshipEvent(models.Model):
    class EventType(models.TextChoices):
        INVITE_SENT = "invite_sent", "Invite sent"
        INVITE_ACCEPTED = "invite_accepted", "Invite accepted"
        INVITE_DECLINED = "invite_declined", "Invite declined"
        INVITE_EXPIRED = "invite_expired", "Invite expired"
        INVITE_CANCELLED = "invite_cancelled", "Invite cancelled"
        MATCH_STARTED = "match_started", "Match started"
        MATCH_PAUSED = "match_paused", "Match paused"
        MATCH_RESUMED = "match_resumed", "Match resumed"
        SHIPS_LOCKED = "ships_locked", "Ships locked"
        SHOT_FIRED = "shot_fired", "Shot fired"
        MATCH_COMPLETED = "match_completed", "Match completed"
        MATCH_RESIGNED = "match_resigned", "Match resigned"
        MATCH_ABANDONED = "match_abandoned", "Match abandoned"
        REMATCH_REQUESTED = "rematch_requested", "Rematch requested"

    match = models.ForeignKey(
        BattleshipMatch,
        on_delete=models.CASCADE,
        related_name="events",
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="battleship_events",
        blank=True,
        null=True,
    )
    event_type = models.CharField(max_length=32, choices=EventType.choices)
    summary = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.match_id}:{self.event_type}"
