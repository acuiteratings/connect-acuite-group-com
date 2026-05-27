from django.urls import path

from .views import (
    attendance_admin_overview,
    attendance_employee_day_export,
    attendance_export,
    attendance_status,
)


urlpatterns = [
    path("status/", attendance_status, name="attendance-status"),
    path("admin/overview/", attendance_admin_overview, name="attendance-admin-overview"),
    path("export/", attendance_export, name="attendance-export"),
    path("export/employee-day/", attendance_employee_day_export, name="attendance-employee-day-export"),
]
