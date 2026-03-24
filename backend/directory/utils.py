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
