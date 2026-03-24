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
    "Credit Analysis",
    "Financial Modelling",
    "Committee Preparation",
    "Issuer Monitoring",
    "Corporate Ratings",
    "Financial Sector Ratings",
    "Research Writing",
    "Customized Research",
    "Data Operations",
    "Technology",
    "ESG Assessment",
    "Compliance",
    "Quality Control",
    "Rating Administration",
    "Client Servicing",
    "Business Development",
    "Marketing Outreach",
    "Training Delivery",
    "Mentoring",
    "Presentation Design",
    "Workflow Design",
    "Power BI",
    "Excel",
    "Python",
]


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
