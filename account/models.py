from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    other_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=250, blank=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.name = self.name.strip().title()
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"

    STATUS_CHOICES = [
        (DRAFT, "Draft"),
        (PUBLISHED, "Published"),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PUBLISHED,
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="posts"
    )

    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, editable=False)

    content = models.TextField()

    image = models.ImageField(upload_to="posts/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.title = self.title.strip()
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 2
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.title}"
