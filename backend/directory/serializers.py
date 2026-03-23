from accounts.serializers import serialize_user


def serialize_directory_profile(profile):
    payload = serialize_user(profile.user)
    payload.update(
        {
            "manager": profile.manager.full_name if profile.manager else None,
            "company_name": profile.company_name,
            "gender": profile.gender,
            "function_name": profile.function_name,
            "city": profile.city,
            "office_location": profile.office_location,
            "work_mode": profile.work_mode,
            "phone_extension": profile.phone_extension,
            "mobile_number": profile.mobile_number,
            "bio": profile.bio,
            "expertise": profile.expertise,
            "skills": profile.skills,
            "joined_on": profile.joined_on.isoformat() if profile.joined_on else None,
            "profile_visible": profile.is_visible,
        }
    )
    return payload
