import logging

from django.urls import reverse
from rest_framework import status

from comicsdb.models.credits import Role
from comicsdb.serializers import RoleSerializer
from users.tests.case_base import TestCaseBase


class GetAllRoleTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls._create_user()

        cls.editor = Role.objects.create(name="Editor", order=1)
        Role.objects.create(name="Editor in Chief", order=2)
        Role.objects.create(name="Artist", order=10)
        return super().setUpTestData()

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self._client_login()

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("api:role-list"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_role_list_view(self):
        response = self.client.get(reverse("api:role-list"))
        serializer = RoleSerializer(self.editor)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(response.data["next"], None)
        self.assertEqual(response.data["previous"], None)
        self.assertEqual(response.data["results"][0], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        resp = self.client.get(reverse("api:arc-list"))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
