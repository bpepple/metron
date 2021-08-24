from django.urls import path

from comicsdb.views.contact import email_view, success_view

app_name = "contact"
urlpatterns = [
    path("email/", email_view, name="email"),
    path("success/", success_view, name="success"),
]
