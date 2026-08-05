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
from django.core.paginator import Paginator
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


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(author=request.user)
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "blog/create_post.html", {"form": form})


def home(request):
    posts = Post.objects.filter(status=Post.PUBLISHED).order_by("-created_at")
    return render(request, "blog/home.html", {"posts": posts})


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = PostForm(instance=post)
    return render(request, "blog/edit_post.html", {"form": form, "post": post})


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)

    if request.method == "POST":
        post.delete()
        return redirect("home")

    return render(request, "blog/delete_post.html", {"post": post})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post_detail.html", {"post": post})


def home(request):
    posts = Post.objects.filter(status="published").order_by("-created_at")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    return render(request, "blog/home.html", {"posts": posts})


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
