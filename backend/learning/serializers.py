def serialize_book(book, *, requester=None):
    requester_open = getattr(book, "requester_has_open", None)
    if requester_open is None:
        requester_open = False
    if requester and getattr(requester, "is_authenticated", False) and requester_open is False:
        requester_open = book.requisitions.filter(
            requester=requester,
            status__in=book.requisitions.model.open_statuses(),
        ).exists()

    available_copies = getattr(book, "available_copies_annotated", None)
    if available_copies is None:
        available_copies = book.available_copies

    open_requisition_count = getattr(book, "open_requisition_count_annotated", None)
    if open_requisition_count is None:
        open_requisition_count = book.open_requisition_count

    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "summary": book.summary,
        "total_copies": book.total_copies,
        "open_requisition_count": open_requisition_count,
        "available_copies": available_copies,
        "is_active": book.is_active,
        "can_request": available_copies > 0 and not requester_open,
        "requester_has_open_requisition": requester_open,
        "created_at": book.created_at.isoformat(),
        "updated_at": book.updated_at.isoformat(),
    }


def serialize_requisition(requisition):
    return {
        "id": requisition.id,
        "status": requisition.status,
        "note": requisition.note,
        "admin_note": requisition.admin_note,
        "requested_at": requisition.requested_at.isoformat(),
        "reviewed_at": requisition.reviewed_at.isoformat() if requisition.reviewed_at else None,
        "issued_at": requisition.issued_at.isoformat() if requisition.issued_at else None,
        "returned_at": requisition.returned_at.isoformat() if requisition.returned_at else None,
        "book": {
            "id": requisition.book_id,
            "title": requisition.book.title,
            "author": requisition.book.author,
        },
        "requester": {
            "id": requisition.requester_id,
            "name": requisition.requester.full_name,
            "email": requisition.requester.email,
        },
    }
