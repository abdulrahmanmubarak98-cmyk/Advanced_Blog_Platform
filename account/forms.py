from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Tag
from django import forms
from django.utils.text import slugify
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(UserCreationForm):
    # This explicitly makes all the field a requirement on the front-end excluding other_name
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    other_name = forms.CharField(required=False)
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

    def clean_email(self):


        # Get the email submitted by the user
        email = self.cleaned_data.get('email')
        
        # Check if a user with this email already exists in the  database ignoring case sensitivity
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        
            # Return the validated email so django can keep it inside cleaned_data
        return email


    def generate_username(self, first_name, last_name): 

            base_username = slugify(f"{first_name}.{last_name}")

            username = base_username
            counter = 1

            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            return username

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
                    "placeholder": "Enter your other name (optional)",
                }
            )

            self.fields["email"].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "Enter your email",
                }
            )

            self.fields["password1"].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "Create a password",
                }
            )

            self.fields["password2"].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "Confirm your password",
                }
            )

    def save(self, commit=True):
        # Obtain user object instance without writing to DB yet
        user = super().save(commit=False)

        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]

        user.username = self.generate_username(first_name, last_name)

        user.first_name = first_name
        user.last_name = last_name
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

            profile = user.profile
            profile.other_name = self.cleaned_data["other_name"]
            profile.save()

        return user

class EmailAuthenticationForm(AuthenticationForm):
    # Replace Django's username input with an email input field for authentication
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email",}),)

    # Keep Django's existing password field, but customize it appearance.
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter your password",}),)


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
