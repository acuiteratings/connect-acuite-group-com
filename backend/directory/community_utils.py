COMMUNITY_CLUB_LIBRARY = [
    {
        "key": "reading_club",
        "label": "Reading Club",
        "description": "For employees who enjoy books, essays, and thoughtful reading discussions.",
        "form": {
            "primary_field_label": "Book Title",
            "primary_field_type": "text",
            "headline_label": "Headline",
            "body_label": "Body",
            "extra_field_label": "Writeup about the book",
            "extra_field_type": "textarea",
        },
    },
    {
        "key": "movie_club",
        "label": "Movie Club",
        "description": "For film lovers who want to share recommendations and discuss movies together.",
        "form": {
            "primary_field_label": "Movie Name",
            "primary_field_type": "text",
            "headline_label": "Headline",
            "body_label": "Body",
            "extra_field_label": "Proposed Date & Time",
            "extra_field_type": "datetime",
        },
    },
    {
        "key": "travel_club",
        "label": "Travel Club",
        "description": "For people who like sharing trips, itineraries, and travel experiences.",
        "form": {
            "primary_field_label": "Destination Name",
            "primary_field_type": "text",
            "headline_label": "Headline",
            "body_label": "Body",
            "extra_field_label": "Proposed Date & Time",
            "extra_field_type": "datetime",
        },
    },
    {
        "key": "entertainment_club",
        "label": "Entertainment Club",
        "description": "For casual fun around shows, music, events, and light social activities.",
        "form": {
            "primary_field_label": "Event Name",
            "primary_field_type": "text",
            "headline_label": "Headline",
            "body_label": "Body",
            "extra_field_label": "Proposed Date & Time",
            "extra_field_type": "datetime",
        },
    },
    {
        "key": "quiz_club",
        "label": "Quiz Club",
        "description": "For employees who enjoy trivia, quizzes, and a friendly challenge.",
        "form": {
            "primary_field_label": "Quiz Topic",
            "primary_field_type": "text",
            "headline_label": "Headline",
            "body_label": "Body",
            "extra_field_label": "Proposed Date & Time",
            "extra_field_type": "datetime",
        },
    },
    {
        "key": "debate_club",
        "label": "Debate Club",
        "description": "For structured discussion, argument, and thoughtful exchange of views.",
        "form": {
            "primary_field_label": "Event Name",
            "primary_field_type": "text",
            "headline_label": "Headline",
            "body_label": "Body",
            "extra_field_label": "Proposed Date & Time",
            "extra_field_type": "datetime",
        },
    },
    {
        "key": "technology_club",
        "label": "Technology Club",
        "description": "For sharing ideas, trends, tools, and experiments in technology.",
        "form": {
            "primary_field_label": "Project Name",
            "primary_field_type": "text",
            "headline_label": "Headline",
            "body_label": "Body",
            "extra_field_label": "Proposed Date & Time",
            "extra_field_type": "datetime",
        },
    },
    {
        "key": "photography_club",
        "label": "Photography Club",
        "description": "For people who enjoy photography, visual storytelling, and photo walks.",
        "form": {
            "primary_field_label": "Album Name",
            "primary_field_type": "text",
            "headline_label": "Headline",
            "body_label": "Body",
            "extra_field_label": "Google link to Photos",
            "extra_field_type": "url",
        },
    },
    {
        "key": "cricket_club",
        "label": "Cricket Club",
        "description": "For employees interested in playing, watching, or organising cricket activities.",
        "form": {
            "primary_field_label": "Event Name",
            "primary_field_type": "text",
            "headline_label": "Headline",
            "body_label": "Body",
            "extra_field_label": "Proposed Date & Time",
            "extra_field_type": "datetime",
        },
    },
    {
        "key": "football_club",
        "label": "Football Club",
        "description": "For employees interested in football matches, chats, and meetups.",
        "form": {
            "primary_field_label": "Event Name",
            "primary_field_type": "text",
            "headline_label": "Headline",
            "body_label": "Body",
            "extra_field_label": "Proposed Date & Time",
            "extra_field_type": "datetime",
        },
    },
    {
        "key": "charity_club",
        "label": "Charity Club",
        "description": "For volunteering, giving initiatives, and social impact activities.",
        "form": {
            "primary_field_label": "Event Name",
            "primary_field_type": "text",
            "headline_label": "Headline",
            "body_label": "Body",
            "extra_field_label": "Proposed Date & Time",
            "extra_field_type": "datetime",
        },
    },
    {
        "key": "health_club",
        "label": "Health Club",
        "description": "For wellbeing, fitness, healthy routines, and supportive health habits.",
        "form": {
            "primary_field_label": "Event Name",
            "primary_field_type": "text",
            "headline_label": "Headline",
            "body_label": "Body",
            "extra_field_label": "Proposed Date & Time",
            "extra_field_type": "datetime",
        },
    },
]

COMMUNITY_CLUB_KEYS = {item["key"] for item in COMMUNITY_CLUB_LIBRARY}
COMMUNITY_CLUB_LOOKUP = {item["key"]: item for item in COMMUNITY_CLUB_LIBRARY}
COMMUNITY_CLUB_LABEL_LOOKUP = {
    item["label"].strip().casefold(): item["key"] for item in COMMUNITY_CLUB_LIBRARY
}


def normalize_community_clubs(value, *, max_items=12):
    cleaned = []
    seen = set()
    for item in value if isinstance(value, (list, tuple)) else []:
        key = str(item or "").strip().lower()
        if not key or key in seen or key not in COMMUNITY_CLUB_KEYS:
            continue
        cleaned.append(key)
        seen.add(key)
        if len(cleaned) >= max_items:
            break
    return cleaned


def normalize_community_hobby_labels(value, *, max_items=12):
    cleaned = []
    seen = set()
    for item in value if isinstance(value, (list, tuple)) else []:
        label = str(item or "").strip()
        if not label:
            continue
        normalized = label.casefold()
        if normalized in seen or normalized not in COMMUNITY_CLUB_LABEL_LOOKUP:
            continue
        cleaned.append(label)
        seen.add(normalized)
        if len(cleaned) >= max_items:
            break
    return cleaned


def community_hobby_labels_to_keys(value, *, max_items=12):
    cleaned = []
    seen = set()
    for item in normalize_community_hobby_labels(value, max_items=max_items):
        key = COMMUNITY_CLUB_LABEL_LOOKUP.get(str(item).strip().casefold())
        if not key or key in seen:
            continue
        cleaned.append(key)
        seen.add(key)
        if len(cleaned) >= max_items:
            break
    return cleaned


def get_community_club_definition(club_key):
    return COMMUNITY_CLUB_LOOKUP.get(str(club_key or "").strip().lower())
