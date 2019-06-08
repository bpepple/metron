from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from comicsdb.models import Team
from comicsdb.serializers import TeamSerializer
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


class GetAllTeamsTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        user = cls._create_user(cls)

        Team.objects.create(name='Teen Titans',
                            slug='teen-titans', edited_by=user)
        Team.objects.create(name='The Avengers',
                            slug='the-avengers', edited_by=user)

    def setUp(self):
        self._client_login()

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:team-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        resp = self.client.get(reverse('api:team-list'))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class GetSingleTeamTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        user = cls._create_user(cls)

        cls.titans = Team.objects.create(
            name='Teen Titans', slug='teen-titans', edited_by=user)
        cls.avengers = Team.objects.create(
            name='The Avengers', slug='the-avengers', edited_by=user)

    def setUp(self):
        self._client_login()

    def test_get_valid_single_team(self):
        response = self.client.get(
            reverse('api:team-detail', kwargs={'pk': self.avengers.pk}))
        team = Team.objects.get(pk=self.avengers.pk)
        serializer = TeamSerializer(team)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_team(self):
        response = self.client.get(
            reverse('api:team-detail', kwargs={'pk': '10'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_view_url(self):
        self.client.logout()
        response = self.client.get(
            reverse('api:team-detail', kwargs={'pk': self.avengers.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
