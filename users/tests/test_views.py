from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from users.forms import CustomUserChangeForm

HTML_REDIRECT_CODE = 301
HTML_OK_CODE = 200


def test_update_profile_view_url_exists_at_desired_location_redirected(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get("/accounts/update")
    assert resp.status_code == HTML_REDIRECT_CODE


def test_update_profile_view_url_exists_at_desired_location(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get("/accounts/update/")
    assert resp.status_code == HTML_OK_CODE


def test_update_profile_view_url_accessible_by_name(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get(reverse("change_profile"))
    assert resp.status_code == HTML_OK_CODE


def test_change_profile_view_uses_correct_template(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get(reverse("change_profile"))
    assert resp.status_code == HTML_OK_CODE
    assertTemplateUsed(resp, "change_profile.html")


def test_update_password_view_url_exists_at_desired_location_redirected(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get("/accounts/password")
    assert resp.status_code == HTML_REDIRECT_CODE


def test_update_password_view_url_exists_at_desired_location(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get("/accounts/password/")
    assert resp.status_code == HTML_OK_CODE


def test_update_password_view_url_accessible_by_name(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get(reverse("change_password"))
    assert resp.status_code == HTML_OK_CODE


def test_change_password_view_uses_correct_template(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get(reverse("change_password"))
    assert resp.status_code == HTML_OK_CODE
    assertTemplateUsed(resp, "change_password.html")


def test_signup_view_url_exists_at_desired_location(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get("/accounts/signup/")
    assert resp.status_code == HTML_OK_CODE


def test_signup_view_url_exists_at_desired_location_redirected(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get("/accounts/signup")
    assert resp.status_code == HTML_REDIRECT_CODE


def test_signup_view_url_accessible_by_name(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get(reverse("signup"))
    assert resp.status_code == HTML_OK_CODE


def test_signup_view_uses_correct_template(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get(reverse("signup"))
    assert resp.status_code == HTML_OK_CODE
    assertTemplateUsed(resp, "signup.html")


def test_profile_view_url_exists_at_desired_location(auto_login_user):
    client, user = auto_login_user()
    resp = client.get(f"/accounts/{user.pk}/")
    assert resp.status_code == HTML_OK_CODE


def test_profile_view_url_exists_at_desired_location_redirected(auto_login_user):
    client, user = auto_login_user()
    resp = client.get(f"/accounts/{user.pk}")
    assert resp.status_code == HTML_REDIRECT_CODE


def test_profile_view_url_accessible_by_name(auto_login_user):
    client, user = auto_login_user()
    resp = client.get(reverse("user-detail", kwargs={"pk": user.pk}))
    assert resp.status_code == HTML_OK_CODE


def test_profile_view_uses_correct_template(auto_login_user):
    client, user = auto_login_user()
    resp = client.get(reverse("user-detail", kwargs={"pk": user.pk}))
    assert resp.status_code == HTML_OK_CODE
    assertTemplateUsed(resp, "users/customuser_detail.html")


def test_valid_form(db):
    form = CustomUserChangeForm(
        data={
            "username": "wsimonson",
            "first_name": "Walter",
            "last_name": "Simonson",
            "email": "wsimonson@test.com",
            "image": "user/walter.jpg",
        }
    )
    assert form.is_valid() is True


def test_form_invalid(db):
    form = CustomUserChangeForm(
        data={
            "username": "",
            "first_name": "bad-data",
            "last_name": "",
            "email": "",
            "image": "",
        }
    )
    assert form.is_valid() is False
