from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from django.contrib.auth import logout

from django.contrib import messages
from .forms import RegisterForm, EmailAuthenticationForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(View):
    def get(self, request):

        # GET requests display an empty registration form.
        form = RegisterForm()
        return render(
            request,
            "accounts/register.html",
            {"form": form},
        )

    def post(self, request):
        # POST requests contain the registration data submitted by the user.
        form = RegisterForm(request.POST)

        # Validate the submitted  registration data.
        if form.is_valid():

            # Create the User and Profile
            user = form.save()

            # Authenticate the user by passing their email as the username and their submitted password.
            user = authenticate(
                username=user.email,
                password=form.cleaned_data["password1"],
            )

            # Automatically log the newly created user in.
            login(request, user)

            # Show a success message.
            messages.success(request, "Welcome " + user.first_name + "!")

            # Send the authenticated user to the homepage
            return redirect("home")

        # If validation fails, display the form again with it erros.
        return render(
            request,
            "accounts/register.html",
            {"form": form},
        )


class LoginView(View):
    def get(self, request):
        form = EmailAuthenticationForm()
        return render(
            request,
            "accounts/login.html",
            {"form": form},
        )

    def post(self, request):
        form = EmailAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Welcome back " + user.first_name + "!")
            return redirect("home")
        # If validation fails, render the same form again
        return render(
            request,
            "accounts/login.html",
            {"form": form},
        )


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):

        # End the user's authenticated session
        logout(request)

        # Send the user back to the login page.
        return redirect("login")
