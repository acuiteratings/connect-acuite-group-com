def serialize_user(user):
    return {
        "id": user.id,
        "email": user.email,
        "name": user.full_name,
        "initials": user.initials,
        "title": user.title,
        "department": user.department,
        "location": user.location,
        "employee_code": user.employee_code,
        "phone_number": user.phone_number,
        "employment_status": user.employment_status,
        "access_level": user.access_level,
        "is_staff": user.is_staff,
        "is_directory_visible": user.is_directory_visible,
        "last_seen_at": user.last_seen_at.isoformat() if user.last_seen_at else None,
        "date_joined": user.date_joined.isoformat() if user.date_joined else None,
    }
