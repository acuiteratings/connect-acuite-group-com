from django.conf import settings
from django.db import models
from django.utils import timezone


class Poll(models.Model):
    question = models.CharField(max_length=220)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    closes_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="voice_polls_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-is_active", "-created_at")

    def __str__(self):
        return self.question

    @property
    def is_open(self):
        return self.is_active and (self.closes_at is None or self.closes_at > timezone.now())


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")
    label = models.CharField(max_length=160)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("position", "id")

    def __str__(self):
        return self.label


class PollVote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="votes")
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name="votes")
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="voice_poll_votes",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("poll", "voter"),
                name="voice_unique_poll_vote_per_voter",
            )
        ]

    def __str__(self):
        return f"{self.voter} -> {self.option}"

