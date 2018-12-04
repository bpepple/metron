from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from comicsdb.models import Publisher
from comicsdb.serializers import PublisherSerializer
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


class GetAllPublisherTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        Publisher.objects.create(name='DC Comics', slug='dc-comics')
        Publisher.objects.create(name='Marvel', slug='marvel')

    def setUp(self):
        self._client_login()

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:publisher-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        resp = self.client.get(reverse('api:publisher-list'))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class GetSinglePublisherTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        cls.dc = Publisher.objects.create(name='DC Comics', slug='dc-comics')
        cls.marvel = Publisher.objects.create(name='Marvel', slug='marvel')

    def setUp(self):
        self._client_login()

    def test_get_valid_single_publisher(self):
        response = self.client.get(
            reverse('api:publisher-detail', kwargs={'pk': self.dc.pk}))
        publisher = Publisher.objects.get(pk=self.dc.pk)
        serializer = PublisherSerializer(publisher)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_publisher(self):
        response = self.client.get(
            reverse('api:publisher-detail', kwargs={'pk': '10'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_view_url(self):
        self.client.logout()
        response = self.client.get(
            reverse('api:publisher-detail', kwargs={'pk': self.dc.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
