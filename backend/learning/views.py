import json

from django.db.models import Count, Exists, F, IntegerField, OuterRef, Q, Value
from django.db.models.functions import Greatest
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from operations.services import record_analytics_event, record_audit_event

from .models import Book, BookRequisition
from .serializers import serialize_book, serialize_requisition


def _parse_json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Request body must be valid JSON.") from exc


def _can_manage_learning(user):
    return user.is_authenticated and (
        user.is_staff or getattr(user, "can_administer_connect", False)
    )


@csrf_exempt
def books_collection(request):
    if request.method == "POST":
        if not _can_manage_learning(request.user):
            return JsonResponse({"detail": "Admin access required."}, status=403)
        try:
            payload = _parse_json_body(request)
        except ValueError as exc:
            return JsonResponse({"detail": str(exc)}, status=400)

        title = str(payload.get("title", "")).strip()
        author = str(payload.get("author", "")).strip()
        if not title or not author:
            return JsonResponse({"detail": "title and author are required."}, status=400)

        book = Book.objects.create(
            catalog_number=str(payload.get("catalog_number", "")).strip(),
            slug=str(payload.get("slug", "")).strip(),
            title=title,
            author=author,
            category=str(payload.get("category", "")).strip(),
            summary=str(payload.get("summary", "")).strip(),
            review_quote=str(payload.get("review_quote", "")).strip(),
            review_source=str(payload.get("review_source", "")).strip(),
            cover_url=str(payload.get("cover_url", "")).strip(),
            office_location=str(payload.get("office_location", "")).strip(),
            shelf_area=str(payload.get("shelf_area", "")).strip(),
            shelf_label=str(payload.get("shelf_label", "")).strip(),
            total_copies=max(1, int(payload.get("total_copies", 1) or 1)),
            is_active=payload.get("is_active", True) is not False,
        )
        record_audit_event(
            action="learning.book_created",
            actor=request.user,
            target=book,
            summary=f"Added library book '{book.title}'",
            metadata={"book_id": book.id},
            request=request,
        )
        return JsonResponse({"book": serialize_book(book, requester=request.user)}, status=201)

    if request.method != "GET":
        return HttpResponseNotAllowed(["GET", "POST"])

    open_statuses = BookRequisition.open_statuses()
    queryset = Book.objects.annotate(
        open_requisition_count_annotated=Count(
            "requisitions",
            filter=Q(requisitions__status__in=open_statuses),
        ),
        available_copies_annotated=Greatest(
            Value(0),
            F("total_copies") - Count(
                "requisitions",
                filter=Q(requisitions__status__in=open_statuses),
            ),
            output_field=IntegerField(),
        ),
    )

    if not _can_manage_learning(request.user):
        queryset = queryset.filter(is_active=True)

    search_query = request.GET.get("q", "").strip()
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) | Q(author__icontains=search_query)
        )

    if request.user.is_authenticated:
        requester_open_subquery = BookRequisition.objects.filter(
            book_id=OuterRef("pk"),
            requester=request.user,
            status__in=open_statuses,
        )
        queryset = queryset.annotate(requester_has_open=Exists(requester_open_subquery))

    books = [serialize_book(book, requester=request.user) for book in queryset]
    requisitions_qs = BookRequisition.objects.all()
    my_open_requests = 0
    if request.user.is_authenticated:
        my_open_requests = BookRequisition.objects.filter(
            requester=request.user,
            status__in=open_statuses,
        ).count()

    return JsonResponse(
        {
            "count": len(books),
            "results": books,
            "summary": {
                "catalog_count": len(books),
                "available_titles": sum(1 for book in books if book["available_copies"] > 0),
                "active_requisitions": requisitions_qs.filter(status__in=open_statuses).count(),
                "my_open_requests": my_open_requests,
            },
        }
    )


@csrf_exempt
def requisitions_collection(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)

    if request.method == "GET":
        queryset = BookRequisition.objects.select_related("book", "requester")
        if not _can_manage_learning(request.user):
            queryset = queryset.filter(requester=request.user)
        requisitions = [serialize_requisition(item) for item in queryset[:100]]
        return JsonResponse({"count": len(requisitions), "results": requisitions})

    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    try:
        payload = _parse_json_body(request)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    book_id = payload.get("book_id")
    if not book_id:
        return JsonResponse({"detail": "book_id is required."}, status=400)

    book = get_object_or_404(Book, pk=book_id, is_active=True)
    if book.available_copies <= 0:
        return JsonResponse({"detail": "This title is currently fully requisitioned."}, status=400)

    if BookRequisition.objects.filter(
        book=book,
        requester=request.user,
        status__in=BookRequisition.open_statuses(),
    ).exists():
        return JsonResponse({"detail": "You already have an open request for this title."}, status=400)

    note = str(payload.get("note", "")).strip()
    requisition = BookRequisition.objects.create(
        book=book,
        requester=request.user,
        note=note[:280],
    )
    record_audit_event(
        action="learning.book_requisition_created",
        actor=request.user,
        target=requisition,
        summary=f"Requested book '{book.title}'",
        metadata={"book_id": book.id},
        request=request,
    )
    record_analytics_event(
        "learning",
        "book_requisition_created",
        actor=request.user,
        metadata={"book_id": book.id, "requisition_id": requisition.id},
        request=request,
    )
    requisition = BookRequisition.objects.select_related("book", "requester").get(pk=requisition.pk)
    return JsonResponse({"requisition": serialize_requisition(requisition)}, status=201)


@csrf_exempt
def requisition_detail(request, requisition_id):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)

    requisition = get_object_or_404(
        BookRequisition.objects.select_related("book", "requester"),
        pk=requisition_id,
    )

    if request.method == "GET":
        if not _can_manage_learning(request.user) and requisition.requester_id != request.user.id:
            return JsonResponse({"detail": "Not found."}, status=404)
        return JsonResponse({"requisition": serialize_requisition(requisition)})

    if request.method != "PATCH":
        return HttpResponseNotAllowed(["GET", "PATCH"])

    if not _can_manage_learning(request.user):
        return JsonResponse({"detail": "Admin access required."}, status=403)

    try:
        payload = _parse_json_body(request)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    status = str(payload.get("status", "")).strip()
    admin_note = str(payload.get("admin_note", "")).strip()[:280]
    valid_statuses = {
        BookRequisition.Status.APPROVED,
        BookRequisition.Status.DECLINED,
        BookRequisition.Status.RETURNED,
        BookRequisition.Status.CANCELLED,
    }
    if status not in valid_statuses:
        return JsonResponse({"detail": "Unsupported requisition status."}, status=400)

    requisition.status = status
    requisition.admin_note = admin_note
    update_fields = ["status", "admin_note", "updated_at"]
    now = timezone.now()
    if status == BookRequisition.Status.APPROVED:
        requisition.reviewed_at = now
        requisition.issued_at = now
        requisition.returned_at = None
        update_fields.extend(["reviewed_at", "issued_at", "returned_at"])
    elif status == BookRequisition.Status.DECLINED:
        requisition.reviewed_at = now
        update_fields.append("reviewed_at")
    elif status == BookRequisition.Status.RETURNED:
        requisition.returned_at = now
        update_fields.append("returned_at")
    requisition.save(update_fields=update_fields)

    record_audit_event(
        action=f"learning.book_requisition_{status}",
        actor=request.user,
        target=requisition,
        summary=f"Marked requisition for '{requisition.book.title}' as {status}",
        metadata={"requisition_id": requisition.id, "status": status},
        request=request,
    )
    record_analytics_event(
        "learning",
        f"book_requisition_{status}",
        actor=request.user,
        metadata={"requisition_id": requisition.id, "book_id": requisition.book_id},
        request=request,
    )
    requisition = BookRequisition.objects.select_related("book", "requester").get(pk=requisition.pk)
    return JsonResponse({"requisition": serialize_requisition(requisition)})
