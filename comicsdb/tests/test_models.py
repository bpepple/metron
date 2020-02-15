import pytest
from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from comicsdb.models import (
    Arc,
    Character,
    Creator,
    Issue,
    Publisher,
    Role,
    Series,
    SeriesType,
    Team,
)

from .case_base import TestCaseBase

HTTP_200_OK = 200


@pytest.mark.django_db
def test_team_model(api_client, team_fixture):
    resp = api_client.get(team_fixture.get_absolute_url())
    assert resp.status_code == HTTP_200_OK
    assert str(team_fixture._meta.verbose_name_plural) == "teams"
    assert isinstance(team_fixture, Team)
    assert str(team_fixture) == team_fixture.name


@pytest.mark.django_db
def test_character_model(api_client, character_fixture):
    resp = api_client.get(character_fixture.get_absolute_url())
    assert resp.status_code == HTTP_200_OK
    assert str(character_fixture._meta.verbose_name_plural) == "characters"
    assert isinstance(character_fixture, Character)
    assert str(character_fixture) == character_fixture.name


@pytest.mark.django_db
def test_arc_model(api_client, arc_fixture):
    resp = api_client.get(arc_fixture.get_absolute_url())
    assert resp.status_code == HTTP_200_OK
    assert isinstance(arc_fixture, Arc)
    assert str(arc_fixture) == arc_fixture.name
    assert str(arc_fixture._meta.verbose_name_plural) == "arcs"


@pytest.mark.django_db
def test_creator_model(api_client, creator_fixture):
    resp = api_client.get(creator_fixture.get_absolute_url())
    assert resp.status_code == HTTP_200_OK
    assert isinstance(creator_fixture, Creator)
    assert str(creator_fixture) == creator_fixture.name
    assert creator_fixture.name == "Walter Simonson"
    assert str(creator_fixture._meta.verbose_name_plural) == "creators"


@pytest.mark.django_db
def test_role_model(role_fixture):
    assert isinstance(role_fixture, Role)
    assert str(role_fixture) == "writer"
    assert str(role_fixture._meta.verbose_name_plural) == "roles"


class PublisherTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        cls.name = "DC Comics"
        cls.slug = slugify(cls.name)

        cls.publisher = Publisher.objects.create(
            name=cls.name, slug=cls.slug, founded=1934, edited_by=user
        )

        on_going_series = SeriesType.objects.create(name="Ongoing Series")

        Series.objects.create(
            name="Superman",
            slug="superman",
            sort_name="Superman",
            series_type=on_going_series,
            publisher=cls.publisher,
            volume=1,
            year_began=1939,
            edited_by=user,
        )

    def setUp(self):
        self._client_login()

    def test_series_count(self):
        self.assertEqual(self.publisher.series_count, 1)

    def test_publisher_creation(self):
        self.assertTrue(isinstance(self.publisher, Publisher))
        self.assertEqual(str(self.publisher), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.publisher._meta.verbose_name_plural), "publishers")

    def test_absolute_url(self):
        resp = self.client.get(self.publisher.get_absolute_url())
        self.assertEqual(resp.status_code, HTTP_200_OK)


class SeriesTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        publisher = Publisher.objects.create(
            name="DC Comics", slug="dc-comics", edited_by=user
        )
        series_type = SeriesType.objects.create(name="Ongoing Series")
        cls.name = "Superman"
        cls.superman = Series.objects.create(
            name=cls.name,
            slug=slugify(cls.name),
            sort_name=cls.name,
            series_type=series_type,
            publisher=publisher,
            volume=1,
            year_began=1939,
            edited_by=user,
        )

    def setUp(self):
        self._client_login()

    def test_series_creation(self):
        self.assertTrue(isinstance(self.superman, Series))
        self.assertEqual(str(self.superman), "Superman (1939)")

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.superman._meta.verbose_name_plural), "Series")

    def test_absolute_url(self):
        resp = self.client.get(self.superman.get_absolute_url())
        self.assertEqual(resp.status_code, HTTP_200_OK)


class IssueTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        issue_date = timezone.now().date()
        publisher = Publisher.objects.create(
            name="DC Comics", slug="dc-comics", edited_by=user
        )
        series_type = SeriesType.objects.create(name="Ongoing Series")
        cls.series_name = "Superman"
        cls.superman = Series.objects.create(
            name=cls.series_name,
            slug=slugify(cls.series_name),
            sort_name=cls.series_name,
            series_type=series_type,
            publisher=publisher,
            volume=1,
            year_began=1939,
            edited_by=user,
        )

        cls.issue = Issue.objects.create(
            series=cls.superman,
            number="1",
            slug="superman-1939-1",
            cover_date=issue_date,
            edited_by=user,
        )

    def setUp(self):
        self._client_login()

    def test_issue_creation(self):
        self.assertTrue(isinstance(self.issue, Issue))
        self.assertEqual(str(self.issue), "Superman #1")

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.issue._meta.verbose_name_plural), "issues")

    def test_absolute_url(self):
        resp = self.client.get(self.issue.get_absolute_url())
        self.assertEqual(resp.status_code, HTTP_200_OK)

    # This test should be in the SeriesTest but for now let's leave this here.
    def test_issue_count(self):
        issue_count = self.superman.issue_count
        self.assertEqual(issue_count, 1)


class SeriesTypeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.name = "Mini-Series"
        cls.notes = "A short series typically four issues"

        cls.series_type = SeriesType.objects.create(name=cls.name, notes=cls.notes)

    def test_seriestype_creation(self):
        self.assertTrue(isinstance(self.series_type, SeriesType))
        self.assertEqual(str(self.series_type), self.name)
