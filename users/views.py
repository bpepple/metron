import logging

from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import DetailView

from metron.utils import get_recaptcha_auth

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser
from .tokens import account_activation_token
from .utils import send_pushover

logger = logging.getLogger(__name__)


def is_activated(user, token):
    return user is not None and account_activation_token.check_token(user, token)


def account_activation_sent(request):
    return render(request, "registration/account_activation_sent.html")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if not is_activated(user, token):
        return render(request, "registration/account_activation_invalid.html")

    user.is_active = True
    user.email_confirmed = True
    user.save()

    # Add the user to the contributor group.
    contributor_group = Group.objects.get(name="contributor")
    user.groups.add(contributor_group)

    login(request, user)
    # Send pushover notification tha user activated account
    send_pushover(f"{user} activated their account on Metron.")
    logger.info(f"{user} activated their account on Metron")

    return redirect("home")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            result = get_recaptcha_auth(request)

            if result["success"]:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = "Activate Your Metron Account"
                message = render_to_string(
                    "registration/account_activation_email.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                    },
                )
                user.email_user(subject, message)
                # Let's send a pushover notice that a user requested an account.
                send_pushover(f"{user} signed up for an account on Metron.")
                logger.info(f"{user} signed up for an account on Metron")

            return redirect("account_activation_sent")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            return redirect("change_password")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "change_password.html", {"form": form})


def change_profile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your profile was successfully updated!")
            return redirect("change_profile")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, "change_profile.html", {"form": form})


class UserProfile(DetailView):
    model = CustomUser
