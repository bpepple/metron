from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from comicsdb.models import Series, SeriesType, Publisher, Issue
from comicsdb.serializers import SeriesSerializer
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


class GetAllSeriesTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        publisher_obj = Publisher.objects.create(name='DC Comics',
                                                 slug='dc-comics')
        series_type_obj = SeriesType.objects.create(name='Cancelled')
        Series.objects.create(name='Superman', slug='superman', publisher=publisher_obj,
                              year_began=1939, series_type=series_type_obj)
        Series.objects.create(name='Batman', slug='batman', publisher=publisher_obj,
                              year_began=1940, series_type=series_type_obj)

    def setUp(self):
        self._client_login()

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:series-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        resp = self.client.get(reverse('api:series-list'))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class GetSingleSeriesTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        cls._create_user(cls)

        factory = APIRequestFactory()
        request = factory.get('/')

        cls.serializer_context = {
            'request': Request(request),
        }

        publisher_obj = Publisher.objects.create(name='Marvel', slug='marvel')
        series_type_obj = SeriesType.objects.create(name='Cancelled')
        cls.thor = Series.objects.create(name='The Mighty Thor', slug='the-mighty-thor',
                                         publisher=publisher_obj, year_began=1965,
                                         series_type=series_type_obj)
        Issue.objects.create(slug='thor-1', cover_date=timezone.now().date(),
                             number='1', series=cls.thor)

    def setUp(self):
        self._client_login()

    def test_get_valid_single_issue(self):
        resp = self.client.get(
            reverse('api:series-detail', kwargs={'pk': self.thor.pk}))
        series = Series.objects.get(pk=self.thor.pk)
        serializer = SeriesSerializer(series, context=self.serializer_context)
        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        response = self.client.get(
            reverse('api:series-detail', kwargs={'pk': self.thor.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
