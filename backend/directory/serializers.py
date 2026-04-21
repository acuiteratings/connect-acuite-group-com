from accounts.serializers import serialize_user

from .utils import resolve_branch_location


def serialize_directory_profile(profile, *, coin_balance=None):
    payload = serialize_user(profile.user)
    payload.update(
        {
            "manager": profile.manager.full_name if profile.manager else None,
            "company_name": profile.company_name,
            "gender": profile.gender,
            "function_name": profile.function_name,
            "department_for_connect": profile.department_for_connect,
            "city": profile.city,
            "office_location": profile.office_location,
            "branch_location": resolve_branch_location(
                profile.city,
                profile.office_location,
                profile.user.location,
            ),
            "work_mode": profile.work_mode,
            "phone_extension": profile.phone_extension,
            "mobile_number": profile.mobile_number,
            "bio": profile.bio,
            "expertise": profile.expertise,
            "skills": profile.skills,
            "hobbies": profile.hobbies,
            "interests": profile.interests,
            "profile_photos": profile.profile_photos,
            "joined_on": profile.joined_on.isoformat() if profile.joined_on else None,
            "profile_visible": profile.is_visible,
            "coin_balance": coin_balance or {},
        }
    )
    return payload
