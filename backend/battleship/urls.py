from django.urls import path

from .views import (
    candidates,
    invite_collection,
    lobby,
    match_cancel,
    match_fire,
    match_placement,
    match_rematch,
    match_resign,
    match_respond,
    match_state,
)

urlpatterns = [
    path("lobby/", lobby, name="battleship-lobby"),
    path("candidates/", candidates, name="battleship-candidates"),
    path("invite/", invite_collection, name="battleship-invite"),
    path("matches/<int:match_id>/state/", match_state, name="battleship-match-state"),
    path("matches/<int:match_id>/respond/", match_respond, name="battleship-match-respond"),
    path("matches/<int:match_id>/cancel/", match_cancel, name="battleship-match-cancel"),
    path("matches/<int:match_id>/placement/", match_placement, name="battleship-match-placement"),
    path("matches/<int:match_id>/fire/", match_fire, name="battleship-match-fire"),
    path("matches/<int:match_id>/resign/", match_resign, name="battleship-match-resign"),
    path("matches/<int:match_id>/rematch/", match_rematch, name="battleship-match-rematch"),
]
