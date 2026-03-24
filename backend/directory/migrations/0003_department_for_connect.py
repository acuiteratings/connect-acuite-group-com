from django.db import migrations, models


def _map_department_for_connect(raw_department):
    department = str(raw_department or "").strip()
    if department in {
        "Administration",
        "Compliance",
        "Finance And Accounts",
        "Human Resource",
    }:
        return "Corporate"
    if department in {
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
    }:
        return "Rating Operations"
    if department in {
        "Corporate Sector Ratings",
        "Client Servicing",
        "Financial Sector Ratings",
        "Marketing And Outreach",
        "SMERA Business Development",
        "Sales",
    }:
        return "Business Development"
    return ""


def populate_department_for_connect(apps, schema_editor):
    DirectoryProfile = apps.get_model("directory", "DirectoryProfile")
    for profile in DirectoryProfile.objects.select_related("user").all():
        mapped_value = _map_department_for_connect(getattr(profile.user, "department", ""))
        if mapped_value != profile.department_for_connect:
            profile.department_for_connect = mapped_value
            profile.save(update_fields=["department_for_connect"])


class Migration(migrations.Migration):

    dependencies = [
        ("directory", "0002_directoryprofile_company_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="directoryprofile",
            name="department_for_connect",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.RunPython(populate_department_for_connect, migrations.RunPython.noop),
    ]
