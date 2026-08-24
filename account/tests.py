from django.test import TestCase
from django.contrib.auth.models import User

from .models import Post, Category, Tag


class TagModelTest(TestCase):

    def test_tag_generates_slug_automatically(self):
        tag = Tag.objects.create(name="Django")

        self.assertEqual(tag.slug, "django")

    def test_tag_normalizes_name(self):
        tag = Tag.objects.create(name="   django   ")

        self.assertEqual(tag.name, "Django")
        self.assertEqual(tag.slug, "django")


class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        self.category = Category.objects.create(
            name="Programming",
            slug="programming",
        )

    def test_post_generates_slug_automatically(self):
        post = Post.objects.create(
            author=self.user,
            category=self.category,
            title="Learning Django",
            content="Learning Django production standards.",
        )

        self.assertEqual(post.slug, "learning-django")

    def test_post_slug_does_not_change_when_title_changes(self):
        post = Post.objects.create(
            author=self.user,
            category=self.category,
            title="Learning Django",
            content="Learning django production standards.",
        )

        original_slug = post.slug
        post.title = "Advanced Django Production Standards"
        post.save()
        self.assertEqual(post.slug, original_slug)
