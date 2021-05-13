from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path(
        "account_activation_sent/",
        views.account_activation_sent,
        name="account_activation_sent",
    ),
    path(
        "activate/(?<uidb64>[0-9A-Za-z_\-]+)/(?<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
        views.activate,
        name="activate",
    ),
    path("password/", views.change_password, name="change_password"),
    path("update/", views.change_profile, name="change_profile"),
    path("<int:pk>/", views.UserProfile.as_view(), name="user-detail"),
]
