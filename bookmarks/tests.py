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
