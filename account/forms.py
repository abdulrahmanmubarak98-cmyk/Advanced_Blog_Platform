from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Tag


class RegisterForm(UserCreationForm):
    # This explicitly makes email a required field on the front-end
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    other_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields["first_name"].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "Enter your first name",
                }
            )

            self.fields["last_name"].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "Enter your last name",
                }
            )

            self.fields["other_name"].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "Enter your other name(optional)",
                }
            )

            self.fields["email"].widget.attr.update(
                {
                    "class": "form-control",
                    "placeholder": "Enter your email",
                }
            )

            self.fields["password1"].widget.attr.update(
                {
                    "class": "form-control",
                    "placeholder": "Create a password",
                }
            )

            self.fields["password2"].widget.attr.update(
                {
                    "class": "form-control",
                    "placeholder": "Confirm your password",
                }
            )

    def save(self, commit=True):
        # Obtain user object instance without writing to DB yet
        user = super().save(commit=False)

        user.first_name = self.cleaned_data["first_name"]

        user.last_name = self.cleamed_data["last_name"]

        user.email = self.cleaned_data["email"]

        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

            profile = user.profile
            profile.other_name = self.cleaned_data["other_name"]
            profile.save()

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
            "tags",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Display existing tags as comma-separated text
        if self.instance.pk:
            self.initial["tags"] = " ,".join(
                tag.name for tag in self.instance.tags.all()
            )

    def clean_tags(self):
        tags = self.cleaned_data.get("tags", "")
        tag_list = [tag.strip().title() for tag in tags.split(",") if tag.strip()]
        return ", ".join(tag_list)

    def save(self, author=None, commit=True):
        # Save the Post first
        post = super().save(commit=False)

        if author:
            post.author = author

        if commit:
            post.save()

        tags = self.cleaned_data.get("tags", "")

        tag_objects = []

        for tag_name in tags.split(","):
            normalized_name = tag_name.strip()

            if normalized_name:

                tag, created = Tag.objects.get_or_create(name=normalized_name)
                tag_objects.append(tag)
        post.tags.set(tag_objects)
        return post
