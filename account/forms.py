from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Tag


class RegisterForm(UserCreationForm):
    # This explicitly makes email a required field on the front-end
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        # Obtain user object instance without writing to DB yet
        user = super().save(commit=False)

        # Pull sanitized email string from Django's validated data
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=255,
        required=False,
        help_text="Separate tags with commas (e.g. python, django, programming)",
    )

    class Meta:
        model = Post
        fields = (
            "category",
            "title",
            "content",
            "image",
            "status",
            "slug",
            "tags",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Display existing tags as comma-separated text
        if self.instance.pk:
            self.fields["tags"].initial = ", ".join(
                tag.name for tag in self.instance.tags.all()
            )

    def save(self, author=None, commit=True):
        # Save the Post first
        post = super().save(commit=False)

        tags = self.cleaned_data.get("tags", "")
        if author:
            post.author = author

        if commit:
            post.save()

            # Remove all old tags
            post.tags.clear()

        # Add the new tags
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]

            tag_objects = []

            for tag_name in tag_list:
                normalized_name = tag_name.strip().title()
                tag, created = Tag.objects.get_or_create(
                    name=normalized_name,
                )
                tag_objects.append(tag)
            post.tags.set(tag_objects)

        return post
