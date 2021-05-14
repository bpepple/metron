from users.models import CustomUser
from users.tests.case_base import TestCaseBase


class CustomUserTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls._create_user()

    def setUp(self):
        self._client_login()

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, CustomUser))
        self.assertEqual(str(self.user), self.user.username)
