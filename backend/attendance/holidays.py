from __future__ import annotations

from datetime import date

from directory.utils import normalize_branch_location


HOLIDAY_CALENDAR_2026 = [
    {
        "sr_no": 1,
        "name": "New Year",
        "day_of_week": "Thursday",
        "date": date(2026, 1, 1),
        "applicability": "All Offices",
        "applicable_locations": [],
        "category": "Festive",
        "state_holiday": "PAN India",
    },
    {
        "sr_no": 2,
        "name": "Pongal",
        "day_of_week": "Wednesday",
        "date": date(2026, 1, 15),
        "applicability": "Chennai, Hyderabad",
        "applicable_locations": ["Chennai", "Hyderabad"],
        "category": "Festive",
        "state_holiday": "Tamil Nadu, Telangana",
    },
    {
        "sr_no": 3,
        "name": "Birth of Netaji",
        "day_of_week": "Friday",
        "date": date(2026, 1, 23),
        "applicability": "Kolkata",
        "applicable_locations": ["Kolkata"],
        "category": "Mandatory - West Bengal State",
        "state_holiday": "West Bengal",
    },
    {
        "sr_no": 4,
        "name": "Republic Day",
        "day_of_week": "Monday",
        "date": date(2026, 1, 26),
        "applicability": "All Offices",
        "applicable_locations": [],
        "category": "Mandatory - National",
        "state_holiday": "PAN India",
    },
    {
        "sr_no": 5,
        "name": "Holi",
        "day_of_week": "Wednesday",
        "date": date(2026, 3, 3),
        "applicability": "Mumbai, Kolkata, Delhi, Ahmedabad",
        "applicable_locations": ["Mumbai", "Kolkata", "Delhi", "Ahmedabad"],
        "category": "Festive",
        "state_holiday": "Maharashtra, West Bengal, Delhi, Gujarat",
    },
    {
        "sr_no": 6,
        "name": "Ugadi",
        "day_of_week": "Friday",
        "date": date(2026, 3, 19),
        "applicability": "Bangalore",
        "applicable_locations": ["Bangalore"],
        "category": "Festive",
        "state_holiday": "Karnataka",
    },
    {
        "sr_no": 7,
        "name": "Eid-al-Fitr",
        "day_of_week": "Saturday",
        "date": date(2026, 3, 21),
        "applicability": "All Offices",
        "applicable_locations": [],
        "category": "Festive",
        "state_holiday": "PAN India",
    },
    {
        "sr_no": 8,
        "name": "Good Friday",
        "day_of_week": "Friday",
        "date": date(2026, 4, 3),
        "applicability": "Mumbai",
        "applicable_locations": ["Mumbai"],
        "category": "Festive",
        "state_holiday": "Maharashtra",
    },
    {
        "sr_no": 9,
        "name": "Tamil New Year",
        "day_of_week": "Tuesday",
        "date": date(2026, 4, 14),
        "applicability": "Chennai",
        "applicable_locations": ["Chennai"],
        "category": "Festive",
        "state_holiday": "Tamil Nadu",
    },
    {
        "sr_no": 10,
        "name": "May / Labour Day",
        "day_of_week": "Friday",
        "date": date(2026, 5, 1),
        "applicability": "All Offices",
        "applicable_locations": [],
        "category": "Mandatory - National",
        "state_holiday": "PAN India",
    },
    {
        "sr_no": 11,
        "name": "Telangana Foundation Day",
        "day_of_week": "Tuesday",
        "date": date(2026, 6, 2),
        "applicability": "Hyderabad",
        "applicable_locations": ["Hyderabad"],
        "category": "Mandatory - Telangana State",
        "state_holiday": "Telangana",
    },
    {
        "sr_no": 12,
        "name": "Independence Day",
        "day_of_week": "Saturday",
        "date": date(2026, 8, 15),
        "applicability": "All Offices",
        "applicable_locations": [],
        "category": "Mandatory - National",
        "state_holiday": "PAN India",
    },
    {
        "sr_no": 13,
        "name": "Janmashtami",
        "day_of_week": "Friday",
        "date": date(2026, 9, 4),
        "applicability": "Delhi",
        "applicable_locations": ["Delhi"],
        "category": "Festive",
        "state_holiday": "Delhi",
    },
    {
        "sr_no": 14,
        "name": "Ganesh Chaturthi",
        "day_of_week": "Monday",
        "date": date(2026, 9, 14),
        "applicability": "Mumbai, Chennai, Hyderabad, Bangalore, Ahmedabad",
        "applicable_locations": ["Mumbai", "Chennai", "Hyderabad", "Bangalore", "Ahmedabad"],
        "category": "Festive",
        "state_holiday": "Maharashtra, Tamil Nadu, Telangana, Karnataka, Gujarat",
    },
    {
        "sr_no": 15,
        "name": "Gandhi Jayanti",
        "day_of_week": "Friday",
        "date": date(2026, 10, 2),
        "applicability": "All Offices",
        "applicable_locations": [],
        "category": "Mandatory - National",
        "state_holiday": "PAN India",
    },
    {
        "sr_no": 16,
        "name": "Durgapuja Nabami",
        "day_of_week": "Monday",
        "date": date(2026, 10, 19),
        "applicability": "Kolkata",
        "applicable_locations": ["Kolkata"],
        "category": "Festive",
        "state_holiday": "West Bengal",
    },
    {
        "sr_no": 17,
        "name": "Dussehra",
        "day_of_week": "Tuesday",
        "date": date(2026, 10, 20),
        "applicability": "All Offices",
        "applicable_locations": [],
        "category": "Festive",
        "state_holiday": "PAN India",
    },
    {
        "sr_no": 18,
        "name": "Diwali (Laxmi Pujan)",
        "day_of_week": "Sunday",
        "date": date(2026, 11, 8),
        "applicability": "All Offices",
        "applicable_locations": [],
        "category": "Festive",
        "state_holiday": "PAN India",
    },
    {
        "sr_no": 19,
        "name": "Vikram Samvat New Year",
        "day_of_week": "Tuesday",
        "date": date(2026, 11, 10),
        "applicability": "Ahmedabad",
        "applicable_locations": ["Ahmedabad"],
        "category": "Festive",
        "state_holiday": "Gujarat",
    },
    {
        "sr_no": 20,
        "name": "Karnataka Day",
        "day_of_week": "Sunday",
        "date": date(2026, 11, 1),
        "applicability": "Bangalore",
        "applicable_locations": ["Bangalore"],
        "category": "Mandatory - Karnataka State",
        "state_holiday": "Karnataka",
    },
    {
        "sr_no": 21,
        "name": "Guru Nanak Jayanti",
        "day_of_week": "Tuesday",
        "date": date(2026, 11, 24),
        "applicability": "Delhi",
        "applicable_locations": ["Delhi"],
        "category": "Festive",
        "state_holiday": "Delhi",
    },
    {
        "sr_no": 22,
        "name": "Christmas",
        "day_of_week": "Friday",
        "date": date(2026, 12, 25),
        "applicability": "All Offices",
        "applicable_locations": [],
        "category": "Festive",
        "state_holiday": "PAN India",
    },
]


def _normalize_location(value):
    return normalize_branch_location(value).casefold()


def holiday_applies_to_location(holiday, location=""):
    if not holiday.get("applicable_locations"):
        return True
    normalized_location = _normalize_location(location)
    if not normalized_location:
        return False
    return normalized_location in {
        _normalize_location(applicable_location)
        for applicable_location in holiday.get("applicable_locations", [])
    }


def serialize_holiday(holiday):
    return {
        "sr_no": holiday["sr_no"],
        "name": holiday["name"],
        "day_of_week": holiday["day_of_week"],
        "date": holiday["date"].isoformat(),
        "applicability": holiday["applicability"],
        "applicable_locations": list(holiday["applicable_locations"]),
        "applies_to_all_offices": not bool(holiday["applicable_locations"]),
        "category": holiday["category"],
        "state_holiday": holiday["state_holiday"],
    }


def holiday_records_for_year(year=2026, location=""):
    records = [
        holiday
        for holiday in HOLIDAY_CALENDAR_2026
        if holiday["date"].year == year
    ]
    if location:
        records = [
            holiday
            for holiday in records
            if holiday_applies_to_location(holiday, location)
        ]
    return sorted(records, key=lambda holiday: (holiday["date"], holiday["sr_no"]))


def holiday_for_date(target_date, location=""):
    normalized_location = _normalize_location(location)
    for holiday in holiday_records_for_year(target_date.year):
        if holiday["date"] == target_date:
            if normalized_location:
                if holiday_applies_to_location(holiday, normalized_location):
                    return holiday
            elif not holiday.get("applicable_locations"):
                return holiday
    return None


def holiday_export_payload(*, year=2026, location=""):
    records = holiday_records_for_year(year, location=location)
    return {
        "year": year,
        "location": normalize_branch_location(location) if location else "",
        "count": len(records),
        "holidays": [serialize_holiday(holiday) for holiday in records],
    }
