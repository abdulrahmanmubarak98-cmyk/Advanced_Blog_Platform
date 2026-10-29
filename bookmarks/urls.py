from django.urls import path
from . import views

urlpatterns = [
    # ... your other URLs ...
    path("post/<slug:slug>/bookmark/", views.toggle_bookmark, name="toggle_bookmark"),
]
