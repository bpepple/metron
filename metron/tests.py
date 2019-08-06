from django.test import TestCase

from users.models import CustomUser

HTML_OK_CODE = 200


class TestCaseBase(TestCase):
    @classmethod
    def _create_user(self):
        user = CustomUser.objects.create(username="brian", email="brian@test.com")
        user.set_password("1234")
        user.save()

        return user

    def _client_login(self):
        self.client.login(username="brian", password="1234")


class TestMetron(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

    def setUp(self):
        self._client_login()

    def test_api_docs_url_exists_at_desired_location(self):
        resp = self.client.get("/docs/")
        self.assertEqual(resp.status_code, HTML_OK_CODE)
