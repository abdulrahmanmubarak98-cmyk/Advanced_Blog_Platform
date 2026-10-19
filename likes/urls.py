from django.urls import path
from . import views

urlpatterns = [
    path("posts/<slug:slug>/like/", views.likes, name="like_post"),
]
