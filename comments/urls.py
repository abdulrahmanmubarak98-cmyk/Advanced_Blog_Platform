from django.urls import path
from . import views

urlpatterns = [
    path(
        "posts/<slug:slug>/comment/",
        views.add_comment,
        name="add_comment",
    ),
]
