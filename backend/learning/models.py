from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=220)
    author = models.CharField(max_length=180)
    summary = models.TextField(blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("title", "author")

    def __str__(self):
        return f"{self.title} - {self.author}"

    @property
    def open_requisition_count(self):
        return self.requisitions.filter(
            status__in=BookRequisition.open_statuses()
        ).count()

    @property
    def available_copies(self):
        return max(0, self.total_copies - self.open_requisition_count)


class BookRequisition(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        APPROVED = "approved", "Approved"
        ISSUED = "issued", "Issued"
        RETURNED = "returned", "Returned"
        DECLINED = "declined", "Declined"
        CANCELLED = "cancelled", "Cancelled"

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="requisitions")
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="book_requisitions",
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.REQUESTED,
    )
    note = models.CharField(max_length=280, blank=True)
    admin_note = models.CharField(max_length=280, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    issued_at = models.DateTimeField(blank=True, null=True)
    returned_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-requested_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("book", "requester"),
                condition=Q(status__in=("requested", "approved", "issued")),
                name="learning_unique_open_book_requisition",
            )
        ]

    def __str__(self):
        return f"{self.requester} - {self.book} ({self.status})"

    @classmethod
    def open_statuses(cls):
        return [cls.Status.REQUESTED, cls.Status.APPROVED, cls.Status.ISSUED]

    def mark_reviewed(self, status, admin_note=""):
        self.status = status
        self.admin_note = admin_note
        self.reviewed_at = timezone.now()
        self.save(update_fields=["status", "admin_note", "reviewed_at", "updated_at"])

