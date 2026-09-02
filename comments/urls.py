from django.urls import path
from . import views

urlpatterns = [
    path(
        "posts/<slug:slug>/comment/",
        views.add_comment,
        name="add_comment",
    ),
    path(
        "comments/<int:comment_id>/delete/",
        views.delete_comment,
        name="delete_comment",
    ),
]
