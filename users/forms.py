from typing import Any, Dict

from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput, EmailField, EmailInput, Textarea, TextInput

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = EmailField(
        max_length=254,
        help_text="Required. Enter a valid email address.",
        required=True,
    )

    def clean(self) -> Dict[str, Any]:
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return super().clean()

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    email = EmailField(
        max_length=254,
        help_text="Required. Enter a valid email address.",
        required=True,
        widget=EmailInput(attrs={"class": "input"}),
        error_messages={"required": "Please provide valid email."},
    )

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "bio", "image")
        widgets = {
            "username": TextInput(attrs={"class": "input"}),
            "first_name": TextInput(attrs={"class": "input"}),
            "last_name": TextInput(attrs={"class": "input"}),
            "bio": Textarea(attrs={"class": "textarea"}),
            "image": ClearableFileInput(),
        }
