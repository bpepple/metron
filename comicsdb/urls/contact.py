from django.urls import path

from comicsdb.views.contact import EmailView, SuccessView


app_name = "contact"
urlpatterns = [
    path("email/", EmailView, name="email"),
    path("success/", SuccessView, name="success"),
]
