from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.utils.translation import ngettext

from users.forms import CustomUserChangeForm, CustomUserCreationForm
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("username", "email", "is_active", "email_confirmed", "date_joined")
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "email_confirmed",
        "date_joined",
        "groups",
    )
    actions = ["grant_add_creator_perm"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "bio", "image")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "email_confirmed",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    @admin.action(description="Grant 'add creator' permission to user")
    def grant_add_creator_perm(self, request, queryset) -> None:
        count = 0
        try:
            permission = Permission.objects.get(name="Can add creator")
        except Permission.DoesNotExist:
            permission = None

        if permission is not None:
            for i in queryset:
                modified = False
                if permission not in i.user_permissions.all():
                    i.user_permissions.add(permission)
                    modified = True

                if modified:
                    count += 1

            self.message_user(
                request,
                ngettext(
                    "%d user was updated.",
                    "%d users were updated.",
                    count,
                )
                % count,
                messages.SUCCESS,
            )
