from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from account.models import Post
from .models import Comment
from django.http import HttpResponseForbidden


@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect("post_detail", slug=post.slug)
        else:
            form = CommentForm()
    return render(
        request,
        "blog/post_detail.html",
        {"form": form, "post": post},
    )


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.user and request.user != comment.post.author:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    if request.method == "POST":
        comment.delete()
        return redirect("post_detail", slug=comment.post.slug)
    return render(
        request,
        "comments/delete_comment.html",
        {"comment": comment},
    )
