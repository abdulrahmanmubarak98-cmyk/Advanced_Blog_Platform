from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from account.models import Post
from .models import Bookmark
from django.http import JsonResponse


@login_required
def saved_posts(request):
    # Retrieve only bookmarks belonging to the logged-in user.
    bookmarks = Bookmark.objects.filter(user=request.user).select_related(
        "post", "post__author", "post__category"
    )

    # Display the bookmarked posts.
    return render(
        request,
        "bookmarks/saved_posts.html",
        {"bookmarks": bookmarks},
    )


@login_required
@require_POST
def bookmark_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # create a bookmark or retrieve the existing one.
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        post=post,
    )

    # Remove the bookmark if it already existed.

    if not created:
        bookmark.delete()

        # Return the updated bookmark state.
    return JsonResponse(
        {
            "user_bookmarked": created,
        }
    )
