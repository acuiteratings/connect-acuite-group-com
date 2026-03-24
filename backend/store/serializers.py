def serialize_store_item(item, *, active_redemptions=0):
    available_units = max(item.stock_units - active_redemptions, 0)
    return {
        "id": item.id,
        "name": item.name,
        "category": item.category,
        "category_label": item.get_category_display(),
        "description": item.description,
        "point_cost": item.point_cost,
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
        "item": {
            "id": redemption.item.id,
            "name": redemption.item.name,
            "category": redemption.item.category,
            "category_label": redemption.item.get_category_display(),
        },
        "points_locked": redemption.points_locked,
        "notes": redemption.notes,
        "created_at": redemption.created_at.isoformat(),
        "updated_at": redemption.updated_at.isoformat(),
    }
