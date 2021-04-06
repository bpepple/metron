import copy

from comicsdb.models import Issue, Publisher, Series, SeriesType
from comicsdb.serializers import SeriesSerializer
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from .case_base import TestCaseBase


class GetAllSeriesTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        publisher_obj = Publisher.objects.create(
            name="DC Comics", slug="dc-comics", edited_by=user
        )
        series_type_obj = SeriesType.objects.create(name="Cancelled")
        Series.objects.create(
            name="Superman",
            slug="superman",
            publisher=publisher_obj,
            volume="1",
            year_began=1939,
            series_type=series_type_obj,
            edited_by=user,
        )
        Series.objects.create(
            name="Batman",
            slug="batman",
            publisher=publisher_obj,
            volume="1",
            year_began=1940,
            series_type=series_type_obj,
            edited_by=user,
        )

    def setUp(self):
        self._client_login()

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("api:series-list"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        resp = self.client.get(reverse("api:series-list"))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class GetSingleSeriesTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        factory = APIRequestFactory()
        cls.request = factory.get("/")

        publisher_obj = Publisher.objects.create(
            name="Marvel", slug="marvel", edited_by=user
        )
        series_type_obj = SeriesType.objects.create(name="Cancelled")
        cls.thor = Series.objects.create(
            name="The Mighty Thor",
            slug="the-mighty-thor",
            publisher=publisher_obj,
            volume="1",
            year_began=1965,
            series_type=series_type_obj,
            edited_by=user,
        )
        Issue.objects.create(
            slug="thor-1",
            cover_date=timezone.now().date(),
            number="1",
            series=cls.thor,
            edited_by=user,
        )

    def setUp(self):
        self._client_login()

    def test_get_valid_single_issue(self):
        test_context = {"request": Request(self.request)}
        thor = copy.deepcopy(self.thor)
        resp = self.client.get(reverse("api:series-detail", kwargs={"pk": thor.pk}))
        series = Series.objects.get(pk=thor.pk)
        serializer = SeriesSerializer(series, context=test_context)
        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        response = self.client.get(
            reverse("api:series-detail", kwargs={"pk": self.thor.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
