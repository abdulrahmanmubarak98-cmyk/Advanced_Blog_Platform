from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm  # Fixed import path
from django.contrib.auth.models import User


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
    class Meta:
        model = Post
        fields = ("category", "title", "content", "image", "status", "slug", "tags")
