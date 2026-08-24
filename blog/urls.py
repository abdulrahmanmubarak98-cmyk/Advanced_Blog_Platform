from django.urls import path
from . import views

urlpatterns = [
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("post/<slug:slug>/edit/", views.edit_post, name="edit_post"),
    path("post/<slug:slug>/delete/", views.delete_post, name="delete_post"),
    path("", views.home, name="home"),
    path("posts/create/", views.create_post, name="create_post"),
]
