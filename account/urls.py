from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("posts/create/", views.create_post, name="create_post"),
    path("", views.home, name="home"),
]
