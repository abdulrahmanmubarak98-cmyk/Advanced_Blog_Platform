from django.shortcuts import render, redirect, get_object_or_404
from account.forms import PostForm
from django.core.paginator import Paginator
from comments.forms import CommentForm
from django.db.models import Q
from account.models import Post
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


# Create a new post.
class CreatePostView(LoginRequiredMixin, View):

    # Display an empty form
    def get(self, request):
        form = PostForm()
        return render(request, "blog/create_post.html", {"form": form})

    # Process submitted form data.
    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # post created successfully with authenticated logged-in user as author of post
            form.save(author=request.user)
            return redirect("home")
        # show form again with error if form is invalid.
        return render(request, "blog/create_post.html", {"form": form})


# Editing an existing post
class EditPostView(LoginRequiredMixin, View):

    # Display the existing post in the form.
    def get(self, request, slug):

        # Find the post using its slug
        # author=request.user is a authorization check. The logged-in user must own the post
        # If no matching post exists, Django returns HTTP 404.
        post = get_object_or_404(Post, slug=slug, author=request.user)

        # instance=post tells Django:
        # This form represents this EXISTING Post object.
        # Therefore the form is populated with the post's
        # Currenr value instead of being empty.
        form = PostForm(instance=post)

        # Send both the form and the post to the template.
        return render(request, "blog/edit_post.html", {"form": form, "post": post})

    # POST handles the submitted changes
    def post(self, request, slug):
        # Retrieve the existing post aagain.
        # Post request must also be protected.  A user must not be able to bypass authorization
        # simply by manually sending a POST.
        post = get_object_or_404(Post, slug=slug, author=request.user)

        # Create a bound form using:
        # request.POST submitted text/data
        # request.FILES uploaded files
        # instance=post the existing database record to update
        # Because an existing instance is supplied, save() will
        # Update that object rather than create a new post
        form = PostForm(request.POST, request.FILES, instance=post)

        # Validate the submitted changes.
        if form.is_valid():

            # Update the existing post
            form.save(author=request.user)

            # Editing succeeded. Redirects the browser to the homepage
            return redirect("home")

        # Validation failed.
        # Return the bound form so the user can see the errors
        # and correct the submitted data.
        return render(request, "blog/edit_post.html", {"form": form, "post": post})


# Delete a post
class DeletePostView(LoginRequiredMixin, View):
    # GET does NOT delete anything
    # Its job is to display the confirmation page
    def get(self, request, slug):

        # Find the post and makes sure the logged-in user owns it
        post = get_object_or_404(Post, slug=slug, author=request.user)

        # Show the delete confirmation page
        return render(
            request,
            "blog/delete_post.html",
            {"post": post},
        )

    # POST performs the destructive operation
    def post(self, request, slug):

        # Retrieve the post and verify ownership before deletion.
        post = get_object_or_404(Post, slug=slug, author=request.user)

        # Permanently remove the Post object from the database.
        post.delete()

        # After successful deletion, return to the homepage.
        return redirect("home")


# Displays a single post and its comments
class PostDetailView(View):

    # Only GET is needed because this view displays a post.
    def get(self, request, slug):
        # Retrieve the requested post using its slug
        # There is no author=request.user because post detail pages are publicly accessible
        post = get_object_or_404(Post, slug=slug)

        # Retrieve all Comment objects related to this particular post.
        # post.comments comes from the relationship defined on
        # the Comment model.
        comments = post.comments.all()

        # Create an empty CommentForm
        # This allows the template to display the comment form.
        form = CommentForm()

        # Send all three pieces of data to the template:
        # post---- the post being viewed
        # comments--- comments belonging to that post
        # form---- empty form for submitting a comment
        return render(
            request,
            "blog/post_detail.html",
            {
                "post": post,
                "form": form,
                "comments": comments,
            },
        )


# Displays published posts with pagination
class HomeView(View):

    # The homepage only needs to handle GET
    def get(self, request):

        # Query the database for published posts
        # order_by() displays the post from newest to oldest
        posts = Post.objects.filter(status="published").order_by("-created_at")

        # Create a paginator that divides the QuerySet into pages containing 5 posts each.
        paginator = Paginator(posts, 5)

        # GET requested page number fromm the URL
        page_number = request.GET.get("page")

        # Get the actual page object requested by the user
        posts = paginator.get_page(page_number)

        # Send the Page object to home.html
        return render(
            request,
            "blog/home.html",
            {"posts": posts},
        )


# Search posts by different fields.
class SearchView(View):
    # Search is performed through a GET request
    def get(self, request):
        # Retrieve the value of the "q" parameter from the url
        query = request.GET.get("q")

        # Only search the database if the user actually
        # supplied a search term
        if query:
            # Search across multiple Post fields
            # Q object allow these conditions to be combined
            # using OR logic.
            posts = (
                Post.objects.filter(
                    Q(title__icontains=query)
                    | Q(content__icontains=query)
                    | Q(category__name__icontains=query)
                    | Q(tags__name__icontains=query)
                )
                # distinction
                # prevent the same Post from apppearing
                # multiple times in a results.
                .distinct()
                # show newest matching posts first.
                .order_by("-created_at")
            )
        else:
            # No search term was supplied
            # This is preferable to returning None because the
            # template can still treat "posts" like a QuerySet.
            posts = Post.objects.none()

        # Send both the search results and the original query to the template.
        return render(
            request,
            "blog/search.html",
            {"posts": posts, "query": query},
        )
