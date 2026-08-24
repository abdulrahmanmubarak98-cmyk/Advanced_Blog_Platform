from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from account.models import Post
from account.forms import PostForm
from django.core.paginator import Paginator
from comments.forms import CommentForm


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


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save(author=request.user)
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
    comments = post.comments.all()
    form = CommentForm()
    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "form": form,
            "comments": comments,
        },
    )


def home(request):
    posts = Post.objects.filter(status=Post.PUBLISHED).order_by("-created_at")
    return render(request, "blog/home.html", {"posts": posts})


def home(request):
    posts = Post.objects.filter(status="published").order_by("-created_at")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    return render(request, "blog/home.html", {"posts": posts})
