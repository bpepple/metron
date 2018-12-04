from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from comicsdb.models import Arc
from comicsdb.serializers import ArcSerializer
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


class GetAllArcsTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        Arc.objects.create(name='World War Hulk', slug='world-war-hulk')
        Arc.objects.create(name='Final Crisis', slug='final-crisis')

    def setUp(self):
        self._client_login()

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:arc-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        resp = self.client.get(reverse('api:arc-list'))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class GetSingleArcTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.hulk = Arc.objects.create(
            name='World War Hulk', slug='world-war-hulk')
        cls.crisis = Arc.objects.create(
            name='Final Crisis', slug='final-crisis')

    def setUp(self):
        self._client_login()

    def test_get_valid_single_arc(self):
        response = self.client.get(
            reverse('api:arc-detail', kwargs={'pk': self.hulk.pk}))
        arc = Arc.objects.get(pk=self.hulk.pk)
        serializer = ArcSerializer(arc)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_arc(self):
        response = self.client.get(
            reverse('api:arc-detail', kwargs={'pk': '10'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_view_url(self):
        self.client.logout()
        response = self.client.get(
            reverse('api:arc-detail', kwargs={'pk': self.hulk.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
