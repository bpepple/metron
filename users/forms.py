from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import EmailField

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    email = EmailField(
        max_length=254,
        help_text="Required. Enter a valid email address.",
        required=True,
    )

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "image")
