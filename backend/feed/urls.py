from django.urls import path

from .views import post_comments, posts_collection, toggle_post_reaction

urlpatterns = [
    path("posts/", posts_collection, name="posts-collection"),
    path("posts/<int:post_id>/comments/", post_comments, name="post-comments"),
    path("posts/<int:post_id>/reactions/toggle/", toggle_post_reaction, name="post-reaction-toggle"),
]
