from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend:

    def authenticate(self, request, username=None, password=None, **kwargs):

        # Making the value Django call "username" as the user's email address

        email = username

        # if either credential is missing, authentication cannot continue.

        if email is None or password is None:
            return None

        # Find the user whose email matches the submitted email.
        #iexact makes the comparison case-insensitive.

        try:
            user = User.objects.get(email__iexact=email)

        except User.DoesNotExist:
            return None

        # check whether the submitted password matches the password hash stored for this user.

        if user.check_password(password):

            # make sure this user is allowed to authenticate (i.e. is_active is True)

            if user.is_active:
                return user

            # Authentication fails if the password is incorrect or the user account is not active.
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        