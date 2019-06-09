from django.urls import reverse
from rest_framework import status

from comicsdb.models import Character
from comicsdb.serializers import CharacterSerializer

from .case_base import TestCaseBase


class GetAllCharactersTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        Character.objects.create(
            name='Superman', slug='superman', edited_by=user)
        Character.objects.create(name='Batman', slug='batman', edited_by=user)

    def setUp(self):
        self._client_login()

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:character-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        resp = self.client.get(reverse('api:character-list'))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class GetSingleCharacterTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        cls.hulk = Character.objects.create(
            name='Hulk', slug='hulk', edited_by=user)
        Character.objects.create(name='Thor', slug='thor', edited_by=user)

    def setUp(self):
        self._client_login()

    def test_get_valid_single_character(self):
        response = self.client.get(reverse('api:character-detail',
                                           kwargs={'pk': self.hulk.pk}))
        character = Character.objects.get(pk=self.hulk.pk)
        serializer = CharacterSerializer(character)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_character(self):
        response = self.client.get(reverse('api:character-detail',
                                           kwargs={'pk': '10'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_view_url(self):
        self.client.logout()
        response = self.client.get(reverse('api:character-detail',
                                           kwargs={'pk': self.hulk.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
