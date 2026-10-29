from django.test import TestCase
from django.contrib.auth.models import User
from account.models import Category, Post
from likes.models import Like


class LikeTests(TestCase):
    def setUp(self):
        # Creat a user who will write the post and like it.
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        # Create the category required by Post.
        self.category = Category.objects.create(
            name="Django",
            slug="django",
        )

        # Create a post for the like tests.

        self.post = Post.objects.create(
            author=self.user,
            category=self.category,
            title="Learning Django Testing",
            content="Practicing automated test.",
        )

    def test_post_is_created(self):
        # Confirm the test post exists in the database.

        self.assertEqual(self.post.title, "Learning Django Testing")

    def test_authenticated_user_can_like_post(self):
        # Log in the test user.

        self.client.force_login(self.user)

        # Submit a Post request to the Like endpoint.

        response = self.client.post(f"/posts/{self.post.slug}/like/")

        # Confirm the request succeeded.

        self.assertEqual(response.status_code, 200)

        # Confirm the JSON response reports the updated state.

        self.assertJSONEqual(
            response.content,
            {"user_liked": True, "like_count": 1},
        )

    def test_authenticated_user_can_unlike_post(self):

        # Start with an existing like
        Like.objects.create(
            user=self.user,
            post=self.post,
        )

        # Log in the user and submit the Like form again.

        self.client.force_login(self.user)
        response = self.client.post(f"/posts/{self.post.slug}/like/")

        # Confirm the Like was removed.

        self.assertFalse(
            Like.objects.filter(
                user=self.user,
                post=self.post,
            ).exists()
        )

        # Confirm the response reports zero likes.
        self.assertJSONEqual(
            response.content,
            {"user_liked": False, "like_count": 0},
        )

    def test_anonymous_user_cannot_like_post(self):
        # Submit a Like request without logging in.

        response = self.client.post(f"/posts/{self.post.slug}/like/")

        # Confirm Django redirect the anonymous user.

        self.assertEqual(response.status_code, 302)

        # confirm no like was created.
        self.assertFalse(Like.objects.filter(post=self.post).exists())

    def test_get_request_cannot_like_post(self):
        # Log in because the endpoint requires authentication.
        self.client.force_login(self.user)

        # Attempt to Like the post using GET.
        response = self.client.get(f"/posts/{self.post.slug}/like/")

        # Confirm the endpoint rejects GET requests.
        self.assertEqual(response.status_code, 405)

        # Confirm no Like was created.
        self.assertFalse(
            Like.objects.filter(
                user=self.user,
                post=self.post,
            ).exists()
        )
