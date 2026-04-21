COMMUNITY_CLUB_LIBRARY = [
    {
        "key": "reading_club",
        "label": "Reading Club",
        "description": "For employees who enjoy books, essays, and thoughtful reading discussions.",
    },
    {
        "key": "movie_club",
        "label": "Movie Club",
        "description": "For film lovers who want to share recommendations and discuss movies together.",
    },
    {
        "key": "travel_club",
        "label": "Travel Club",
        "description": "For people who like sharing trips, itineraries, and travel experiences.",
    },
    {
        "key": "entertainment_club",
        "label": "Entertainment Club",
        "description": "For casual fun around shows, music, events, and light social activities.",
    },
    {
        "key": "quiz_club",
        "label": "Quiz Club",
        "description": "For employees who enjoy trivia, quizzes, and a friendly challenge.",
    },
    {
        "key": "debate_club",
        "label": "Debate Club",
        "description": "For structured discussion, argument, and thoughtful exchange of views.",
    },
    {
        "key": "technology_club",
        "label": "Technology Club",
        "description": "For sharing ideas, trends, tools, and experiments in technology.",
    },
    {
        "key": "photography_club",
        "label": "Photography Club",
        "description": "For people who enjoy photography, visual storytelling, and photo walks.",
    },
    {
        "key": "cricket_club",
        "label": "Cricket Club",
        "description": "For employees interested in playing, watching, or organising cricket activities.",
    },
    {
        "key": "football_club",
        "label": "Football Club",
        "description": "For employees interested in football matches, chats, and meetups.",
    },
    {
        "key": "charity_club",
        "label": "Charity Club",
        "description": "For volunteering, giving initiatives, and social impact activities.",
    },
    {
        "key": "health_club",
        "label": "Health Club",
        "description": "For wellbeing, fitness, healthy routines, and supportive health habits.",
    },
]

COMMUNITY_CLUB_KEYS = {item["key"] for item in COMMUNITY_CLUB_LIBRARY}


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
