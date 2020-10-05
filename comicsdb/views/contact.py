import json
import logging
import urllib

from comicsdb.forms.contact import ContactForm
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import get_template
from metron import settings

LOGGER = logging.getLogger(__name__)


def email_view(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            """ Begin reCAPTCHA validation """
            recaptcha_response = request.POST.get("g-recaptcha-response")
            url = "https://www.google.com/recaptcha/api/siteverify"
            values = {
                "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                "response": recaptcha_response,
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            """ End reCAPTCHA validation """

            if result["success"]:
                email = form.cleaned_data["email"]
                subject = form.cleaned_data["subject"]
                message = form.cleaned_data["message"]
                try:
                    send_mail(subject, message, email, ["brian@pepple.info"])
                except BadHeaderError:
                    return HttpResponse("Invalid header found.")

                LOGGER.info(f"{email} sent a contact e-mail")
                return redirect("contact:success")
            else:
                messages.error(request, "Invalid reCAPTCHA. Please try agin.")

                return redirect("contact:email")

    return render(request, "comicsdb/contact-us.html", {"form": form})


def success_view(request):
    success_template = get_template("comicsdb/contact-success.html")
    message = "Success! Thank you for contacting us."
    html = success_template.render({"msg": message})
    return HttpResponse(html)
