from django.urls import path

from .event_views import event_detail, events_collection
from .views import post_comments, post_detail, posts_collection, toggle_post_reaction

urlpatterns = [
    path("events/", events_collection, name="events-collection"),
    path("events/<int:post_id>/", event_detail, name="event-detail"),
    path("posts/", posts_collection, name="posts-collection"),
    path("posts/<int:post_id>/", post_detail, name="post-detail"),
    path("posts/<int:post_id>/comments/", post_comments, name="post-comments"),
    path("posts/<int:post_id>/reactions/toggle/", toggle_post_reaction, name="post-reaction-toggle"),
]
