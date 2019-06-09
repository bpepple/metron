from django.test import TestCase

from users.models import CustomUser


class TestCaseBase(TestCase):
    @classmethod
    def _create_user(self):
        user = CustomUser.objects.create(username="brian", email="brian@test.com")
        user.set_password("1234")
        user.save()

        return user

    def _client_login(self):
        self.client.login(username="brian", password="1234")
