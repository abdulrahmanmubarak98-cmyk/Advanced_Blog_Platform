from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Post
from .models import Tag
from .forms import PostForm
from django.utils.text import slugify

from django.db.models import Q


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


def search(request):
    query = request.GET.get("q")
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(category__name__icontains=query)
            | Q(tags__name__icontains=query).distinct().order_by("-created_at")
        )

    else:
        posts = Post.objects.none()
    return render(
        request,
        "blog/search.html",
        {
            "posts": posts,
            "query": query,
        },
    )
