from django.urls import reverse

from users.forms import CustomUserChangeForm
from users.tests.case_base import TestCaseBase

HTML_REDIRECT_CODE = 301
HTML_OK_CODE = 200


class UserViewTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = cls._create_user()
        return super().setUpTestData()

    def setUp(self) -> None:
        self._client_login()
        return super().setUp()

    def test_update_profile_view_url_exists_at_desired_location_redirected(self):
        resp = self.client.get("/accounts/update")
        self.assertEqual(resp.status_code, HTML_REDIRECT_CODE)

    def test_update_profile_view_url_exists_at_desired_location(self):
        resp = self.client.get("/accounts/update/")
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_update_profile_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("change_profile"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_change_profile_view_uses_correct_template(self):
        resp = self.client.get(reverse("change_profile"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, "change_profile.html")

    def test_update_password_view_url_exists_at_desired_location_redirected(self):
        resp = self.client.get("/accounts/password")
        self.assertEqual(resp.status_code, HTML_REDIRECT_CODE)

    def test_update_password_view_url_exists_at_desired_location(self):
        resp = self.client.get("/accounts/password/")
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_update_password_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("change_password"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_change_password_view_uses_correct_template(self):
        resp = self.client.get(reverse("change_password"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, "change_password.html")

    def test_signup_view_url_exists_at_desired_location(self):
        resp = self.client.get("/accounts/signup/")
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_signup_view_url_exists_at_desired_location_redirected(self):
        resp = self.client.get("/accounts/signup")
        self.assertEqual(resp.status_code, HTML_REDIRECT_CODE)

    def test_signup_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("signup"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_signup_view_uses_correct_template(self):
        resp = self.client.get(reverse("signup"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, "signup.html")

    def test_profile_view_url_exists_at_desired_location(self):
        resp = self.client.get(f"/accounts/{self.user.pk}/")
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_profile_view_url_exists_at_desired_location_redirected(self):
        resp = self.client.get(f"/accounts/{self.user.pk}")
        self.assertEqual(resp.status_code, HTML_REDIRECT_CODE)

    def test_profile_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("user-detail", kwargs={"pk": self.user.pk}))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_profile_view_uses_correct_template(self):
        resp = self.client.get(reverse("user-detail", kwargs={"pk": self.user.pk}))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, "users/customuser_detail.html")


class TestProfileForm(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        cls._create_user()

    def setUp(self):
        self._client_login()

    def test_valid_form(self):
        form = CustomUserChangeForm(
            data={
                "username": "wsimonson",
                "first_name": "Walter",
                "last_name": "Simonson",
                "email": "wsimonson@test.com",
                "image": "user/walter.jpg",
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = CustomUserChangeForm(
            data={
                "username": "",
                "first_name": "bad-data",
                "last_name": "",
                "email": "",
                "image": "",
            }
        )
        self.assertFalse(form.is_valid())
