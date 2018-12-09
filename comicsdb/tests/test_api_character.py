from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from comicsdb.models import Character
from comicsdb.serializers import CharacterSerializer
from users.models import CustomUser


class TestCaseBase(TestCase):

    def _create_user(self):
        user = CustomUser.objects.create(
            username='brian', email='brian@test.com')
        user.set_password('1234')
        user.save()

        return user

    def _client_login(self):
        self.client.login(username='brian', password='1234')


class GetAllCharactersTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        Character.objects.create(name='Superman', slug='superman')
        Character.objects.create(name='Batman', slug='batman')

    def setUp(self):
        self._client_login()

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:character-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        resp = self.client.get(reverse('api:character-list'))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class GetSingleCharacterTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.hulk = Character.objects.create(name='Hulk', slug='hulk')
        Character.objects.create(name='Thor', slug='thor')

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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)