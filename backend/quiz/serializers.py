from django.utils import timezone

from .models import QuizAnswer
from .models import QuizParticipant
from .question_bank import CATEGORY_LABELS, DIFFICULTY_LABELS, get_question_by_key


def serialize_candidate(user):
    return {
        "id": user.id,
        "name": user.full_name,
        "email": user.email,
        "title": user.title,
        "department": user.department,
        "location": user.location,
        "initials": user.initials,
    }


def serialize_match_brief(match, *, viewer=None):
    accepted_count = match.participants.filter(status=QuizParticipant.Status.ACCEPTED).count()
    return {
        "id": match.id,
        "status": match.status,
        "status_label": match.get_status_display(),
        "difficulty": match.difficulty,
        "difficulty_label": DIFFICULTY_LABELS.get(match.difficulty, match.difficulty.title()),
        "host": serialize_candidate(match.host),
        "accepted_count": accepted_count,
        "created_at": match.created_at.isoformat(),
        "started_at": match.started_at.isoformat() if match.started_at else None,
        "completed_at": match.completed_at.isoformat() if match.completed_at else None,
        "viewer_is_host": bool(viewer and getattr(viewer, "pk", None) == match.host_id),
    }


def serialize_match_state(match, viewer):
    participant_map = {item.user_id: item for item in match.participants.select_related("user")}
    viewer_participant = participant_map.get(viewer.id)
    participants = [
        {
            "id": item.id,
            "user": serialize_candidate(item.user),
            "seat": item.seat,
            "status": item.status,
            "score": item.score,
        }
        for item in sorted(participant_map.values(), key=lambda entry: entry.seat)
    ]
    accepted_participants = [item for item in participants if item["status"] == QuizParticipant.Status.ACCEPTED]
    sorted_scores = sorted(accepted_participants, key=lambda item: (-item["score"], item["seat"]))
    current_question = None
    if match.status == match.Status.ACTIVE and match.current_question_key:
        question = get_question_by_key(match.current_question_key)
        now = timezone.now()
        current_answer_count = QuizAnswer.objects.filter(
            match=match,
            question_index=match.current_question_index,
        ).count()
        viewer_answered = bool(
            viewer_participant
            and QuizAnswer.objects.filter(
                match=match,
                participant_id=viewer_participant.id,
                question_index=match.current_question_index,
            ).exists()
        )
        current_question = {
            "index": match.current_question_index + 1,
            "total": match.total_questions,
            "key": question["key"],
            "category": question["category"],
            "category_label": CATEGORY_LABELS.get(question["category"], question["category"].replace("_", " ").title()),
            "difficulty": question["difficulty"],
            "difficulty_label": DIFFICULTY_LABELS.get(question["difficulty"], question["difficulty"].title()),
            "prompt": question["prompt"],
            "options": question["options"],
            "deadline_at": match.question_deadline_at.isoformat() if match.question_deadline_at else None,
            "seconds_remaining": max(
                0,
                int((match.question_deadline_at - now).total_seconds()) if match.question_deadline_at else 0,
            ),
            "answers_received": current_answer_count,
            "viewer_answered": viewer_answered,
        }
    return {
        **serialize_match_brief(match, viewer=viewer),
        "participants": participants,
        "leaderboard": sorted_scores,
        "viewer": {
            "participant_id": viewer_participant.id if viewer_participant else None,
            "status": viewer_participant.status if viewer_participant else "",
            "score": viewer_participant.score if viewer_participant else 0,
            "is_host": match.host_id == viewer.id,
        },
        "current_question": current_question,
    }
