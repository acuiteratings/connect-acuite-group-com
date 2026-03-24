from django.db.models import Count


def serialize_poll(poll, *, voter=None):
    options = list(
        poll.options.annotate(vote_count=Count("votes")).order_by("position", "id")
    )
    total_votes = sum(option.vote_count for option in options)
    voter_option_id = None
    if voter and getattr(voter, "is_authenticated", False):
        vote = poll.votes.filter(voter=voter).values_list("option_id", flat=True).first()
        voter_option_id = vote

    return {
        "id": poll.id,
        "question": poll.question,
        "description": poll.description,
        "is_active": poll.is_active,
        "is_open": poll.is_open,
        "closes_at": poll.closes_at.isoformat() if poll.closes_at else None,
        "total_votes": total_votes,
        "user_vote_option_id": voter_option_id,
        "options": [
            {
                "id": option.id,
                "label": option.label,
                "vote_count": option.vote_count,
                "percent": round((option.vote_count / total_votes) * 100) if total_votes else 0,
            }
            for option in options
        ],
    }

