from django.test import TestCase
from django.contrib.auth import get_user_model

from blog.models import Post, Category


class PostModelTest(TestCase):
    def setUp(self):
        User = get_user_model
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )

        self.category = Category.objects.create(name="Django")
