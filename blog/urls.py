from django.urls import path
from . import views

urlpatterns = [
    path("posts/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<slug:slug>/edit/", views.EditPostView.as_view(), name="edit_post"),
    path(
        "posts/<slug:slug>/delete/", views.DeletePostView.as_view(), name="delete_post"
    ),
    path("", views.HomeView.as_view(), name="home"),
    path("posts/create/", views.CreatePostView.as_view(), name="create_post"),
    path("search/", views.SearchView.as_view(), name="search"),
]
