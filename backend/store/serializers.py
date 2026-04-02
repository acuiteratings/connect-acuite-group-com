def serialize_store_item(item, *, active_redemptions=0):
    available_units = max(item.stock_units - active_redemptions, 0)
    return {
        "id": item.id,
        "name": item.name,
        "category": item.category,
        "category_label": item.get_category_display(),
        "description": item.description,
        "point_cost": item.point_cost,
        "coin_cost": item.point_cost,
        "stock_units": item.stock_units,
        "available_units": available_units,
        "accent_hex": item.accent_hex,
        "image_url": item.image_url,
        "is_active": item.is_active,
    }


def serialize_redemption(redemption):
    return {
        "id": redemption.id,
        "status": redemption.status,
        "status_label": redemption.get_status_display(),
        "item": {
            "id": redemption.item.id,
            "name": redemption.item.name,
            "category": redemption.item.category,
            "category_label": redemption.item.get_category_display(),
        },
        "requester": {
            "id": redemption.requester.id,
            "name": redemption.requester.full_name,
            "email": redemption.requester.email,
        },
        "points_locked": redemption.points_locked,
        "coin_cost": redemption.points_locked,
        "notes": redemption.notes,
        "admin_note": redemption.admin_note,
        "created_at": redemption.created_at.isoformat(),
        "reviewed_at": redemption.reviewed_at.isoformat() if redemption.reviewed_at else None,
        "updated_at": redemption.updated_at.isoformat(),
    }
