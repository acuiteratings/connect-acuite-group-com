from django.urls import path

from .views import candidates, lobby, match_answer, match_cancel, match_respond, match_start, match_state, matches_collection

urlpatterns = [
    path("lobby/", lobby, name="quiz-lobby"),
    path("candidates/", candidates, name="quiz-candidates"),
    path("matches/", matches_collection, name="quiz-matches"),
    path("matches/<int:match_id>/state/", match_state, name="quiz-match-state"),
    path("matches/<int:match_id>/respond/", match_respond, name="quiz-match-respond"),
    path("matches/<int:match_id>/start/", match_start, name="quiz-match-start"),
    path("matches/<int:match_id>/answer/", match_answer, name="quiz-match-answer"),
    path("matches/<int:match_id>/cancel/", match_cancel, name="quiz-match-cancel"),
]
