from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from comicsdb.models import Arc, Publisher, Series, SeriesType, Issue
from comicsdb.serializers import ArcSerializer, IssueListSerializer
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

        publisher_obj = Publisher.objects.create(name='DC Comics',
                                                 slug='dc-comics')
        series_type_obj = SeriesType.objects.create(name='Cancelled')
        series_obj = Series.objects.create(name='Final Crisis', slug='final-crisis',
                                           publisher=publisher_obj, year_began=1939,
                                           series_type=series_type_obj)
        cls.issue_obj = Issue.objects.create(series=series_obj,
                                             number='1',
                                             slug='final-crisis-1',
                                             cover_date=timezone.now().date())
        cls.hulk = Arc.objects.create(name='World War Hulk',
                                      slug='world-war-hulk')
        cls.crisis = Arc.objects.create(name='Final Crisis',
                                        slug='final-crisis')
        cls.issue_obj.arcs.add(cls.crisis)

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
        response = self.client.get(reverse('api:arc-detail',
                                           kwargs={'pk': self.hulk.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_arc_issue_list_view(self):
        response = self.client.get(reverse('api:arc-issue-list',
                                           kwargs={'pk': self.crisis.pk}))
        serializer = IssueListSerializer(self.issue_obj)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(response.data['results'][0], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
