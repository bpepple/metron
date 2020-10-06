import logging

from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from metron.utils import get_recaptcha_auth

from .forms import CustomUserCreationForm
from .models import CustomUser
from .tokens import account_activation_token
from .utils import send_pushover

logger = logging.getLogger(__name__)


def account_activation_sent(request):
    return render(request, "users/account_activation_sent.html")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        # Send pushover notification tha user activated account
        send_pushover(f"{user} activated their account on Metron.")
        logger.info(f"{user} activated their account on Metron")

        return redirect("home")
    else:
        return render(request, "users/account_activation_invalid.html")


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
                subject = "Activate Your MySite Account"
                message = render_to_string(
                    "users/account_activation_email.html",
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
    return render(request, "users/signup.html", {"form": form})
