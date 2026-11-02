from django.urls import path
from . import views

urlpatterns = [
    path(
        "post/<slug:slug>/bookmark/",
        views.bookmark_post,
        name="bookmark_post",
    ),
    # Display the logged-in user's saved posts
    path(
        "saved-post/",
        views.saved_posts,
        name="saved_posts",
    ),
]
