from django.contrib import admin
from django.utils import timezone

from operations.services import record_analytics_event, record_audit_event

from .models import Book, BookRequisition


@admin.action(description="Approve selected requisitions")
def approve_requisitions(_modeladmin, request, queryset):
    for requisition in queryset:
        requisition.mark_reviewed(BookRequisition.Status.APPROVED)
        record_audit_event(
            action="learning.book_requisition_approved",
            actor=request.user,
            target=requisition,
            summary=f"Approved book request for '{requisition.book.title}'",
            request=request,
        )
        record_analytics_event(
            "learning",
            "book_requisition_approved",
            actor=request.user,
            metadata={"requisition_id": requisition.id},
            request=request,
        )


@admin.action(description="Mark selected requisitions as issued")
def issue_requisitions(_modeladmin, request, queryset):
    for requisition in queryset:
        requisition.status = BookRequisition.Status.ISSUED
        requisition.reviewed_at = requisition.reviewed_at or timezone.now()
        requisition.issued_at = timezone.now()
        requisition.save(update_fields=["status", "reviewed_at", "issued_at", "updated_at"])
        record_audit_event(
            action="learning.book_requisition_issued",
            actor=request.user,
            target=requisition,
            summary=f"Issued book '{requisition.book.title}'",
            request=request,
        )


@admin.action(description="Mark selected requisitions as returned")
def return_requisitions(_modeladmin, request, queryset):
    for requisition in queryset:
        requisition.status = BookRequisition.Status.RETURNED
        requisition.returned_at = timezone.now()
        requisition.save(update_fields=["status", "returned_at", "updated_at"])
        record_audit_event(
            action="learning.book_requisition_returned",
            actor=request.user,
            target=requisition,
            summary=f"Returned book '{requisition.book.title}'",
            request=request,
        )


@admin.action(description="Decline selected requisitions")
def decline_requisitions(_modeladmin, request, queryset):
    for requisition in queryset:
        requisition.mark_reviewed(BookRequisition.Status.DECLINED)
        record_audit_event(
            action="learning.book_requisition_declined",
            actor=request.user,
            target=requisition,
            summary=f"Declined book request for '{requisition.book.title}'",
            request=request,
        )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "total_copies", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "author", "summary")


@admin.register(BookRequisition)
class BookRequisitionAdmin(admin.ModelAdmin):
    list_display = ("book", "requester", "status", "requested_at", "updated_at")
    list_filter = ("status", "requested_at")
    search_fields = ("book__title", "book__author", "requester__email", "requester__first_name", "requester__last_name")
    autocomplete_fields = ("book", "requester")
    actions = (approve_requisitions, issue_requisitions, return_requisitions, decline_requisitions)
