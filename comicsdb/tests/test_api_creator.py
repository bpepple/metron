from comicsdb.models import Creator
from comicsdb.serializers import CreatorSerializer
from django.urls import reverse
from rest_framework import status
from users.tests.case_base import TestCaseBase


class GetAllCreatorsTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        Creator.objects.create(name="John Byrne", slug="john-byrne", edited_by=user)
        Creator.objects.create(
            name="Walter Simonson", slug="walter-simonson", edited_by=user
        )

    def setUp(self):
        self._client_login()

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("api:creator-list"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        resp = self.client.get(reverse("api:creator-list"))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class GetSingleCreatorTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        cls.jack = Creator.objects.create(
            name="Jack Kirby", slug="jack-kirby", edited_by=user
        )
        Creator.objects.create(name="Steve Ditko", slug="steve-ditko", edited_by=user)

    def setUp(self):
        self._client_login()

    def test_get_valid_single_creator(self):
        response = self.client.get(
            reverse("api:creator-detail", kwargs={"pk": self.jack.pk})
        )
        creator = Creator.objects.get(pk=self.jack.pk)
        serializer = CreatorSerializer(creator)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_creator(self):
        response = self.client.get(reverse("api:creator-detail", kwargs={"pk": "10"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_view_url(self):
        self.client.logout()
        response = self.client.get(
            reverse("api:creator-detail", kwargs={"pk": self.jack.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
