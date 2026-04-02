import random
from datetime import timedelta

from django.db.models import Q
from django.db import transaction
from django.utils import timezone

from accounts.models import User
from operations.services import record_audit_event

from .models import QuizAnswer, QuizMatch, QuizParticipant
from .question_bank import get_question_by_key, get_questions_for_difficulty

QUESTION_SECONDS = 15
EMPLOYEE_ACCESS_LEVELS = {
    User.AccessLevel.EMPLOYEE,
    User.AccessLevel.MANAGER,
    User.AccessLevel.MODERATOR,
    User.AccessLevel.ADMIN,
}


class QuizRuleError(Exception):
    def __init__(self, message, *, status=400, code="quiz_rule_error"):
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code


def create_event(match, actor, action, summary, request=None):
    record_audit_event(
        action=f"quiz.{action}",
        summary=summary,
        actor=actor,
        target=match,
        metadata={"match_id": match.id},
        request=request,
    )


def get_candidate_users(viewer, query=""):
    queryset = User.objects.filter(
        is_active=True,
        employment_status=User.EmploymentStatus.ACTIVE,
        access_level__in=EMPLOYEE_ACCESS_LEVELS,
    ).exclude(pk=viewer.pk)
    query = str(query or "").strip()
    if len(query) >= 2:
        queryset = queryset.filter(
            Q(email__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(title__icontains=query)
        )
    else:
        queryset = queryset.none()
    return list(queryset.order_by("first_name", "last_name")[:12])


def get_match_queryset():
    return QuizMatch.objects.select_related("host").prefetch_related("participants__user", "answers")


def load_match_for_user(match_id, user):
    match = get_match_queryset().get(pk=match_id)
    if not match.participants.filter(user=user).exists():
        raise QuizRuleError("You are not part of this quiz match.", status=403, code="forbidden_match_access")
    return match


@transaction.atomic
def create_match(host, invitee_user_ids, difficulty, *, request=None):
    difficulty = str(difficulty or "").strip().lower()
    if difficulty not in {choice[0] for choice in QuizMatch.Difficulty.choices}:
        raise QuizRuleError("Choose a valid difficulty level.", code="invalid_difficulty")
    invitee_ids = []
    for raw_id in invitee_user_ids or []:
        try:
            numeric = int(raw_id)
        except (TypeError, ValueError) as exc:
            raise QuizRuleError("Invite list contains an invalid employee.", code="invalid_invitee") from exc
        if numeric != host.id and numeric not in invitee_ids:
            invitee_ids.append(numeric)
    if not invitee_ids:
        raise QuizRuleError("Invite at least one colleague to start a quiz.", code="missing_invitees")
    if len(invitee_ids) > 3:
        raise QuizRuleError("You can invite up to three colleagues.", code="too_many_invitees")

    invitees = list(
        User.objects.filter(
            pk__in=invitee_ids,
            is_active=True,
            employment_status=User.EmploymentStatus.ACTIVE,
            access_level__in=EMPLOYEE_ACCESS_LEVELS,
        )
    )
    if len(invitees) != len(invitee_ids):
        raise QuizRuleError("One or more invited employees could not be found.", status=404, code="invitee_missing")

    match = QuizMatch.objects.create(host=host, difficulty=difficulty)
    QuizParticipant.objects.create(
        match=match,
        user=host,
        seat=1,
        status=QuizParticipant.Status.ACCEPTED,
        joined_at=timezone.now(),
    )
    for seat, invitee in enumerate(invitees, start=2):
        QuizParticipant.objects.create(
            match=match,
            user=invitee,
            seat=seat,
            status=QuizParticipant.Status.INVITED,
        )
    create_event(match, host, "invite_sent", f"Started a quiz invite at {match.get_difficulty_display()}.", request=request)
    return match


@transaction.atomic
def respond_to_invitation(match_id, user, decision, *, request=None):
    decision = str(decision or "").strip().lower()
    if decision not in {"accept", "decline"}:
        raise QuizRuleError("Decision must be accept or decline.", code="invalid_decision")
    match = QuizMatch.objects.select_for_update().get(pk=match_id)
    participant = QuizParticipant.objects.select_for_update().get(match=match, user=user)
    if participant.status != QuizParticipant.Status.INVITED:
        raise QuizRuleError("This invitation has already been handled.", code="invite_already_handled")
    participant.status = QuizParticipant.Status.ACCEPTED if decision == "accept" else QuizParticipant.Status.DECLINED
    participant.joined_at = timezone.now() if decision == "accept" else None
    participant.save(update_fields=["status", "joined_at", "updated_at"])
    create_event(match, user, f"invite_{decision}ed", f"{user.full_name} {decision}ed the quiz invite.", request=request)
    return match


def _accepted_participants(match):
    return list(match.participants.filter(status=QuizParticipant.Status.ACCEPTED).select_related("user"))


@transaction.atomic
def start_match(match_id, user, *, request=None):
    match = QuizMatch.objects.select_for_update().get(pk=match_id)
    if match.host_id != user.id:
        raise QuizRuleError("Only the host can start the quiz.", status=403, code="host_only")
    if match.status != QuizMatch.Status.INVITED:
        raise QuizRuleError("This quiz cannot be started now.", code="invalid_match_state")
    accepted = _accepted_participants(match)
    if len(accepted) < 2:
        raise QuizRuleError("At least two accepted participants are required.", code="not_enough_players")
    available_questions = get_questions_for_difficulty(match.difficulty)
    if len(available_questions) < match.total_questions:
        raise QuizRuleError("Question bank is not ready for this difficulty.", code="question_bank_short")

    chosen = random.sample(available_questions, match.total_questions)
    now = timezone.now()
    match.status = QuizMatch.Status.ACTIVE
    match.question_order = [item["key"] for item in chosen]
    match.current_question_index = 0
    match.current_question_key = chosen[0]["key"]
    match.question_started_at = now
    match.question_deadline_at = now + timedelta(seconds=QUESTION_SECONDS)
    match.started_at = now
    match.save(
        update_fields=[
            "status",
            "question_order",
            "current_question_index",
            "current_question_key",
            "question_started_at",
            "question_deadline_at",
            "started_at",
            "updated_at",
        ]
    )
    match.participants.filter(status=QuizParticipant.Status.INVITED).update(status=QuizParticipant.Status.DECLINED)
    create_event(match, user, "started", f"{user.full_name} started the quiz.", request=request)
    return match


def _finalize_match(match):
    scores = list(match.participants.filter(status=QuizParticipant.Status.ACCEPTED).order_by("-score", "seat"))
    match.status = QuizMatch.Status.COMPLETED
    match.completed_at = timezone.now()
    match.question_deadline_at = None
    match.save(update_fields=["status", "completed_at", "question_deadline_at", "updated_at"])
    return scores


@transaction.atomic
def advance_match_if_needed(match_id):
    match = QuizMatch.objects.select_for_update().prefetch_related("participants__user", "answers").get(pk=match_id)
    if match.status != QuizMatch.Status.ACTIVE or not match.question_deadline_at:
        return match
    now = timezone.now()
    accepted_ids = list(match.participants.filter(status=QuizParticipant.Status.ACCEPTED).values_list("id", flat=True))
    answered_count = QuizAnswer.objects.filter(
        match=match,
        question_index=match.current_question_index,
        participant_id__in=accepted_ids,
    ).count()
    if answered_count < len(accepted_ids) and now < match.question_deadline_at:
        return match

    next_index = match.current_question_index + 1
    if next_index >= len(match.question_order):
        _finalize_match(match)
        return match

    match.current_question_index = next_index
    match.current_question_key = match.question_order[next_index]
    match.question_started_at = now
    match.question_deadline_at = now + timedelta(seconds=QUESTION_SECONDS)
    match.save(
        update_fields=[
            "current_question_index",
            "current_question_key",
            "question_started_at",
            "question_deadline_at",
            "updated_at",
        ]
    )
    return match


@transaction.atomic
def answer_question(match_id, user, selected_option, *, request=None):
    match = advance_match_if_needed(match_id)
    match = QuizMatch.objects.select_for_update().prefetch_related("participants__user").get(pk=match.pk)
    if match.status != QuizMatch.Status.ACTIVE:
        raise QuizRuleError("This quiz is not active now.", code="match_not_active")
    participant = QuizParticipant.objects.select_for_update().get(match=match, user=user)
    if participant.status != QuizParticipant.Status.ACCEPTED:
        raise QuizRuleError("Only accepted players can answer.", status=403, code="player_not_active")
    now = timezone.now()
    if not match.question_deadline_at or now > match.question_deadline_at:
        raise QuizRuleError("This question has already closed.", code="question_closed")
    if QuizAnswer.objects.filter(match=match, participant=participant, question_index=match.current_question_index).exists():
        raise QuizRuleError("You already answered this question.", code="already_answered")
    question = get_question_by_key(match.current_question_key)
    option = str(selected_option or "").strip().upper()
    if option not in {"A", "B", "C", "D"}:
        raise QuizRuleError("Choose one of the four options.", code="invalid_option")
    response_ms = max(0, int((now - match.question_started_at).total_seconds() * 1000)) if match.question_started_at else None
    is_correct = option == question["correct_option"]
    QuizAnswer.objects.create(
        match=match,
        participant=participant,
        question_index=match.current_question_index,
        question_key=question["key"],
        selected_option=option,
        is_correct=is_correct,
        response_ms=response_ms,
    )
    if is_correct:
        participant.score += 1
        participant.save(update_fields=["score", "updated_at"])
    create_event(match, user, "answered", f"{user.full_name} answered a quiz question.", request=request)
    return advance_match_if_needed(match_id)


@transaction.atomic
def cancel_match(match_id, user, *, request=None):
    match = QuizMatch.objects.select_for_update().get(pk=match_id)
    if match.host_id != user.id:
        raise QuizRuleError("Only the host can cancel the quiz.", status=403, code="host_only")
    if match.status not in {QuizMatch.Status.INVITED, QuizMatch.Status.ACTIVE}:
        raise QuizRuleError("This quiz cannot be cancelled now.", code="invalid_match_state")
    match.status = QuizMatch.Status.CANCELLED
    match.question_deadline_at = None
    match.save(update_fields=["status", "question_deadline_at", "updated_at"])
    create_event(match, user, "cancelled", f"{user.full_name} cancelled the quiz.", request=request)
    return match
