from django.urls import reverse

from users.forms import CustomUserChangeForm

HTML_REDIRECT_CODE = 301
HTML_OK_CODE = 200


def test_update_profile_view_url_exists_at_desired_location_redirected(loggedin_user):
    resp = loggedin_user.get("/accounts/update")
    assert resp.status_code == HTML_REDIRECT_CODE


def test_update_profile_view_url_exists_at_desired_location(loggedin_user):
    resp = loggedin_user.get("/accounts/update/")
    assert resp.status_code == HTML_OK_CODE


def test_update_profile_view_url_accessible_by_name(loggedin_user):
    resp = loggedin_user.get(reverse("change_profile"))
    assert resp.status_code == HTML_OK_CODE


def test_change_profile_view_uses_correct_template(loggedin_user):
    resp = loggedin_user.get(reverse("change_profile"))
    assert resp.status_code == HTML_OK_CODE
    assert "change_profile.html" in (t.name for t in resp.templates)


def test_update_password_view_url_exists_at_desired_location_redirected(loggedin_user):
    resp = loggedin_user.get("/accounts/password")
    assert resp.status_code == HTML_REDIRECT_CODE


def test_update_password_view_url_exists_at_desired_location(loggedin_user):
    resp = loggedin_user.get("/accounts/password/")
    assert resp.status_code == HTML_OK_CODE


def test_update_password_view_url_accessible_by_name(loggedin_user):
    resp = loggedin_user.get(reverse("change_password"))
    assert resp.status_code == HTML_OK_CODE


def test_change_password_view_uses_correct_template(loggedin_user):
    resp = loggedin_user.get(reverse("change_password"))
    assert resp.status_code == HTML_OK_CODE
    assert "change_password.html" in (t.name for t in resp.templates)


def test_signup_view_url_exists_at_desired_location(loggedin_user):
    resp = loggedin_user.get("/accounts/signup/")
    assert resp.status_code == HTML_OK_CODE


def test_signup_view_url_exists_at_desired_location_redirected(loggedin_user):
    resp = loggedin_user.get("/accounts/signup")
    assert resp.status_code == HTML_REDIRECT_CODE


def test_signup_view_url_accessible_by_name(loggedin_user):
    resp = loggedin_user.get(reverse("signup"))
    assert resp.status_code == HTML_OK_CODE


def test_signup_view_uses_correct_template(loggedin_user):
    resp = loggedin_user.get(reverse("signup"))
    assert resp.status_code == HTML_OK_CODE
    assert "signup.html" in (t.name for t in resp.templates)


def test_profile_view_url_exists_at_desired_location(loggedin_user, user):
    resp = loggedin_user.get(f"/accounts/{user.pk}/")
    assert resp.status_code == HTML_OK_CODE


def test_profile_view_url_exists_at_desired_location_redirected(loggedin_user, user):
    resp = loggedin_user.get(f"/accounts/{user.pk}")
    assert resp.status_code == HTML_REDIRECT_CODE


def test_profile_view_url_accessible_by_name(loggedin_user, user):
    resp = loggedin_user.get(reverse("user-detail", kwargs={"pk": user.pk}))
    assert resp.status_code == HTML_OK_CODE


def test_profile_view_uses_correct_template(loggedin_user, user):
    resp = loggedin_user.get(reverse("user-detail", kwargs={"pk": user.pk}))
    assert resp.status_code == HTML_OK_CODE
    assert "users/customuser_detail.html" in (t.name for t in resp.templates)


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
