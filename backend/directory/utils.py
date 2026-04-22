import re


CORPORATE_DEPARTMENTS = {
    "Administration",
    "Compliance",
    "Finance And Accounts",
    "Human Resource",
}

RATING_OPERATIONS_DEPARTMENTS = {
    "Analytical Operations",
    "SMERA Rating Operations",
    "Technology",
    "Customized Research",
    "Data Operations",
    "ESG Assessment",
    "Not Applicable",
    "Quality Control",
    "Rating Administration",
    "Rating Committee Operations",
    "Issuer Monitoring",
}

BUSINESS_DEVELOPMENT_DEPARTMENTS = {
    "Corporate Sector Ratings",
    "Client Servicing",
    "Financial Sector Ratings",
    "Marketing And Outreach",
    "SMERA Business Development",
    "Sales",
}

CONNECT_DEPARTMENT_LABELS = [
    "Corporate",
    "Rating Operations",
    "Business Development",
]

PROFILE_SKILL_LIBRARY = [
    "MS Excel",
    "PowerBI",
    "Python & SQL",
    "Rating Criteria",
    "Rating Modelling",
    "Financial Forecasting",
    "Economic Forecasting",
    "Business Writing",
    "Creative Writing",
    "Influencing",
    "Public Speaking",
    "Leadership",
    "Quality Management",
]


def normalize_branch_location(raw_location):
    location = str(raw_location or "").strip()
    if not location:
        return ""

    normalized = " ".join(location.replace("_", " ").split())
    lowered = normalized.casefold()

    if lowered in {"ahmedabad", "chennai", "hyderabad", "kolkata"}:
        return normalized.title()

    if lowered in {"bangalore", "bengaluru"}:
        return "Bangalore"

    if lowered in {"new delhi", "delhi"}:
        return "New Delhi"

    if re.fullmatch(r"mumbai(?:\s+\d+)?", lowered):
        return "Mumbai"

    return ""


def resolve_branch_location(*candidates):
    for candidate in candidates:
        normalized = normalize_branch_location(candidate)
        if normalized:
            return normalized
    return ""


def map_department_for_connect(raw_department):
    department = str(raw_department or "").strip()
    if not department:
        return ""
    if department in CORPORATE_DEPARTMENTS:
        return "Corporate"
    if department in RATING_OPERATIONS_DEPARTMENTS:
        return "Rating Operations"
    if department in BUSINESS_DEVELOPMENT_DEPARTMENTS:
        return "Business Development"
    return ""


def normalize_string_list(value, *, max_items=10):
    if isinstance(value, str):
        raw_items = value.replace("\n", ",").split(",")
    elif isinstance(value, (list, tuple)):
        raw_items = value
    else:
        raw_items = []

    cleaned = []
    seen = set()
    for item in raw_items:
        text = str(item or "").strip()
        key = text.casefold()
        if not text or key in seen:
            continue
        cleaned.append(text)
        seen.add(key)
        if len(cleaned) >= max_items:
            break
    return cleaned


def normalize_profile_photos(value, *, max_items=2):
    if not isinstance(value, (list, tuple)):
        return []

    photos = []
    for item in value:
        text = str(item or "").strip()
        if not text:
            continue
        if len(text) > 2_500_000:
            continue
        if text.startswith("data:image/") or text.startswith("https://") or text.startswith("http://"):
            photos.append(text)
        if len(photos) >= max_items:
            break
    return photos
