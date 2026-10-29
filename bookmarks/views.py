from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from account.models import Post
from .models import Bookmark


@login_required
@require_POST
def bookmark_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # create a bookmark or find thr existing one.
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        post=post,
    )

    # Remove the bookmark if it already existed.

    if not created:
        bookmark.delete()

        # Return to the post detail page.
        return redirect("post_detail", slug=post.slug)
