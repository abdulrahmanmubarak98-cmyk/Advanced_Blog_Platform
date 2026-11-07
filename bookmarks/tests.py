# Provides Django's test environment and database isolation
from django.test import TestCase

# Allows us to create a test user
from django.contrib.auth.models import User

# Generates URLs using their URL names
from django.urls import reverse

# Allow us to create a test post
from account.models import Post, Category

# Allows us to inspect bookmark records
from bookmarks.models import Bookmark


class BookmarkTests(TestCase):
    def setUp(self):
        # Create a test user.
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        # Create a category for the test post.
        self.category = Category.objects.create(
            name="Technology",
            slug="technology",
        )

        # Create a test post.
        self.post = Post.objects.create(
            author=self.user,
            category=self.category,
            title="Learning Django",
            content="This is a test.",
        )

    def test_user_can_bookmark_post(self):
        # Log in the test user
        self.client.login(
            username="testuser",
            password="testpassword123",
        )
        # Send a POST request to bookmark the post.
        response = self.client.post(
            reverse("bookmark_post", args=[self.post.slug]),
        )

        # Confirm Django returns a successful JSON response.
        self.assertEqual(response.status_code, 200)

        # Confirm the bookmark was created.
        self.assertTrue(
            Bookmark.objects.filter(user=self.user, post=self.post).exists()
        )

        # Confirm the response reports a saved bookmarked.

        self.assertTrue(response.json()["user_bookmarked"])

    def test_user_can_remove_bookmark(self):

        # Log in test user
        self.client.login(
            username="testuser",
            password="testpassword123",
        )

        # Create an existing book
        Bookmark.objects.create(
            user=self.user,
            post=self.post,
        )

        # Send a POST request to remove the bookmark

        response = self.client.post(reverse("bookmark_post", args=[self.post.slug]))

        # confirm the request succeeds.
        self.assertEqual(response.status_code, 200)

        # Confirm the bookmark was deleted.
        self.assertFalse(
            Bookmark.objects.filter(
                user=self.user,
                post=self.post,
            ).exists()
        )

        # Confirm the response reports an unsaved bookmark
        self.assertFalse(response.json()["user_bookmarked"])

    def test_unauthenticated_user(self):

        # Send a POST request without logging in.
        response = self.client.post(reverse("bookmark_post", args=[self.post.slug]))

        # Confirm the user is redirected to the login page.
        self.assertEqual(response.status_code, 302)

        # Confirm no bookmark was created for the user and post.
        self.assertFalse(
            Bookmark.objects.filter(
                user=self.user,
                post=self.post,
            ).exists()
        )

    def test_get_request_is_rejected(self):

        self.client.login(
            username="testuser",
            password="testpassword123",
        )

        response = self.client.get(reverse("bookmark_post", args=[self.post.slug]))

        self.assertEqual(response.status_code, 405)

        self.assertFalse(
            Bookmark.objects.filter(
                user=self.user,
                post=self.post,
            ).exists()
        )

    def test_user_only_sees_their_own_bookmarks(self):
        # Create a second user.
        second_user = User.objects.create_user(
            username="seconduser",
            password="secondpassword123",
        )

        # Create a post owned by the second user.
        second_post = Post.objects.create(
            author=second_user,
            category=self.category,
            title="A message to my Akhi.",
            content="Inded this method is the best for me to become an independent developer.",
        )

        # Create a bookmark belonging to the first user.
        first_bookmark = Bookmark.objects.create(
            user=self.user,
            post=self.post,
        )

        # Create another bookmark belonging to the second user.
        second_bookmark = Bookmark.objects.create(
            user=second_user,
            post=second_post,
        )

        # Log in as the first user.
        self.client.login(
            username="testuser",
            password="testpassword123",
        )

        # Visit the Saved Posts page.
        response = self.client.get(reverse("saved_posts"))

        # Confirm the page loads successfully.
        self.assertEqual(response.status_code, 200)

        # Retrieve the bookmarks queryset from the template context.
        saved_bookmarks = response.context["bookmarks"]

        # Confirm that only the first user's bookmark is returned.
        self.assertQuerySetEqual(
            saved_bookmarks,
            [first_bookmark.pk],
            transform=lambda bookmark: bookmark.pk,
        )
