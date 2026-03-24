from django.urls import path

from .views import active_poll, vote_on_poll

urlpatterns = [
    path("polls/active/", active_poll, name="voice-active-poll"),
    path("polls/<int:poll_id>/vote/", vote_on_poll, name="voice-vote-on-poll"),
]

