from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from account.models import Post
from .models import Like
from django.views.decorators.http import require_POST
from django.http import JsonResponse


# requires authentication
@login_required
@require_POST
def likes(request, slug):
    # Django retrieves the post using its slug
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":

        # Create a like, or remove the existing one
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post,
        )

        if not created:
            like.delete()

        # Return the updated state without redirecting
        like_count = Like.objects.filter(post=post).count()
        return JsonResponse(
            {
                "user_liked": created,
                "like_count": like_count,
            }
        )
