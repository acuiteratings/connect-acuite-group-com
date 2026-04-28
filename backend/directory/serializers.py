from .utils import resolve_branch_location


def _serialize_directory_user(user, *, include_private_fields=False):
    payload = {
        "id": user.id,
        "email": user.email,
        "name": user.full_name,
        "initials": user.initials,
        "title": user.title,
        "department": user.department,
        "location": user.location,
        "employee_code": user.employee_code,
    }
    if include_private_fields:
        payload["phone_number"] = user.phone_number
    return payload


def serialize_directory_profile(
    profile,
    *,
    coin_balance=None,
    include_profile_photos=False,
    include_private_fields=False,
):
    payload = _serialize_directory_user(
        profile.user,
        include_private_fields=include_private_fields,
    )
    payload.update(
        {
            "manager": profile.manager.full_name if profile.manager else None,
            "company_name": profile.company_name,
            "function_name": profile.function_name,
            "department_for_connect": profile.department_for_connect,
            "city": profile.city,
            "office_location": profile.office_location,
            "branch_location": resolve_branch_location(
                profile.office_location,
                profile.city,
                profile.user.location,
            ),
            "work_mode": profile.work_mode,
            "bio": profile.bio,
            "expertise": profile.expertise,
            "skills": profile.skills,
            "clubs": profile.clubs,
            "hobbies": profile.hobbies,
            "interests": profile.interests,
            "profile_visible": profile.is_visible,
            "coin_balance": coin_balance or {},
        }
    )
    if include_private_fields:
        payload.update(
            {
                "gender": profile.gender,
                "phone_extension": profile.phone_extension,
                "mobile_number": profile.mobile_number,
                "joined_on": profile.joined_on.isoformat() if profile.joined_on else None,
            }
        )
    if include_profile_photos:
        payload["profile_photos"] = profile.profile_photos
    return payload
