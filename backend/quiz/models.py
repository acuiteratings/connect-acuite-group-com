from django.conf import settings
from django.db import models


class QuizMatch(models.Model):
    class Status(models.TextChoices):
        INVITED = "invited", "Invited"
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class Difficulty(models.TextChoices):
        AMATEUR = "amateur", "Amateur"
        ENTHUSIAST = "enthusiast", "Enthusiast"
        PROFESSIONAL = "professional", "Professional"
        EXPERT = "expert", "Expert"

    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_matches_hosted",
    )
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.INVITED)
    difficulty = models.CharField(max_length=24, choices=Difficulty.choices)
    total_questions = models.PositiveSmallIntegerField(default=10)
    current_question_index = models.PositiveSmallIntegerField(default=0)
    current_question_key = models.CharField(max_length=80, blank=True)
    question_order = models.JSONField(default=list, blank=True)
    question_started_at = models.DateTimeField(blank=True, null=True)
    question_deadline_at = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)


class QuizParticipant(models.Model):
    class Status(models.TextChoices):
        ACCEPTED = "accepted", "Accepted"
        INVITED = "invited", "Invited"
        DECLINED = "declined", "Declined"

    match = models.ForeignKey(QuizMatch, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_participations",
    )
    seat = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.INVITED)
    score = models.PositiveIntegerField(default=0)
    joined_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("seat", "created_at")
        constraints = [
            models.UniqueConstraint(fields=["match", "user"], name="quiz_unique_participant_per_match"),
            models.UniqueConstraint(fields=["match", "seat"], name="quiz_unique_seat_per_match"),
        ]


class QuizAnswer(models.Model):
    match = models.ForeignKey(QuizMatch, on_delete=models.CASCADE, related_name="answers")
    participant = models.ForeignKey(
        QuizParticipant,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    question_index = models.PositiveSmallIntegerField()
    question_key = models.CharField(max_length=80)
    selected_option = models.CharField(max_length=1)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)
    response_ms = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ("question_index", "answered_at")
        constraints = [
            models.UniqueConstraint(
                fields=["participant", "question_index"],
                name="quiz_one_answer_per_participant_per_question",
            ),
        ]
