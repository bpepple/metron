import logging

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from comicsdb.models import Issue, Publisher, Series, SeriesType
from comicsdb.serializers import PublisherSerializer, SeriesListSerializer
from users.tests.case_base import TestCaseBase


class GetAllPublisherTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        Publisher.objects.create(name="DC Comics", slug="dc-comics", edited_by=user)
        Publisher.objects.create(name="Marvel", slug="marvel", edited_by=user)

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self._client_login()

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("api:publisher-list"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_url(self):
        self.client.logout()
        resp = self.client.get(reverse("api:publisher-list"))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class GetSinglePublisherTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        cls.dc = Publisher.objects.create(name="DC Comics", slug="dc-comics", edited_by=user)
        cls.marvel = Publisher.objects.create(name="Marvel", slug="marvel", edited_by=user)

        series_type_obj = SeriesType.objects.create(name="Cancelled")
        cls.series_obj = Series.objects.create(
            name="Final Crisis",
            slug="final-crisis",
            publisher=cls.dc,
            volume="1",
            year_began=1939,
            series_type=series_type_obj,
            edited_by=user,
        )
        Issue.objects.create(
            series=cls.series_obj,
            number="1",
            slug="final-crisis-1",
            image="issue/test.jpg",
            cover_date=timezone.now().date(),
            edited_by=user,
        )

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self._client_login()

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_get_valid_single_publisher(self):
        response = self.client.get(reverse("api:publisher-detail", kwargs={"pk": self.dc.pk}))
        publisher = Publisher.objects.get(pk=self.dc.pk)
        serializer = PublisherSerializer(publisher)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_publisher(self):
        response = self.client.get(reverse("api:publisher-detail", kwargs={"pk": "10"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_view_url(self):
        self.client.logout()
        response = self.client.get(reverse("api:publisher-detail", kwargs={"pk": self.dc.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_publisher_series_list_view(self):
        response = self.client.get(
            reverse("api:publisher-series-list", kwargs={"pk": self.dc.pk})
        )
        serializer = SeriesListSerializer(self.series_obj)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["next"], None)
        self.assertEqual(response.data["previous"], None)
        self.assertEqual(response.data["results"][0], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
