from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from comicsdb.models import (Arc, Character, Creator, Issue, Publisher, Role,
                             Series, SeriesType, Team)
from users.models import CustomUser

HTTP_200_OK = 200


class TestCaseBase(TestCase):

    def _create_user(self):
        user = CustomUser.objects.create(
            username='brian', email='brian@test.com')
        user.set_password('1234')
        user.save()

        return user

    def _client_login(self):
        self.client.login(username='brian', password='1234')


class TeamTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        user = cls._create_user(cls)

        cls.name = 'Justice League'
        cls.slug = slugify(cls.name)
        cls.jl = Team.objects.create(
            name=cls.name, slug=cls.slug, edited_by=user)

    def setUp(self):
        self._client_login()

    def test_test_creation(self):
        self.assertTrue(isinstance(self.jl, Team))
        self.assertEqual(str(self.jl), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.jl._meta.verbose_name_plural), 'teams')

    def test_absolute_url(self):
        resp = self.client.get(self.jl.get_absolute_url())
        self.assertEqual(resp.status_code, HTTP_200_OK)


class CharacterTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        user = cls._create_user(cls)

        cls.name = 'Wonder Woman'
        cls.slug = slugify(cls.name)
        cls.ww = Character.objects.create(
            name=cls.name, slug=cls.slug, edited_by=user)

    def setUp(self):
        self._client_login()

    def test_character_creation(self):
        self.assertTrue(isinstance(self.ww, Character))
        self.assertEqual(str(self.ww), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.ww._meta.verbose_name_plural), 'characters')

    def test_absolute_url(self):
        resp = self.client.get(self.ww.get_absolute_url())
        self.assertEqual(resp.status_code, HTTP_200_OK)


class ArcTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        user = cls._create_user(cls)

        cls.name = 'The Last Age of Magic'
        cls.slug = slugify(cls.name)

        cls.arc = Arc.objects.create(
            name=cls.name, slug=cls.slug, edited_by=user)

    def setUp(self):
        self._client_login()

    def test_arc_creation(self):
        self.assertTrue(isinstance(self.arc, Arc))
        self.assertEqual(str(self.arc), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.arc._meta.verbose_name_plural),
                         "arcs")

    def test_absolute_url(self):
        resp = self.client.get(self.arc.get_absolute_url())
        self.assertEqual(resp.status_code, HTTP_200_OK)


class CreatorTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        user = cls._create_user(cls)

        cls.name = 'Walter Simonson'
        cls.slug = 'walter-simonson'
        cls.creator = Creator.objects.create(
            name=cls.name, slug=cls.slug, edited_by=user)

    def setUp(self):
        self._client_login()

    def test_creator_creation(self):
        self.assertTrue(isinstance(self.creator, Creator))
        self.assertEqual(str(self.creator), self.name)

    def test_creator_get_full_name(self):
        self.assertEqual(self.creator.name, self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.creator._meta.verbose_name_plural),
                         'creators')

    def test_absolute_url(self):
        resp = self.client.get(self.creator.get_absolute_url())
        self.assertEqual(resp.status_code, HTTP_200_OK)


class RoleTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.name = 'writer'
        notes = 'Writer of the issues story'
        cls.role = Role.objects.create(name=cls.name, notes=notes, order=20)

    def test_role_creation(self):
        self.assertTrue(isinstance(self.role, Role))
        self.assertEqual(str(self.role), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.role._meta.verbose_name_plural), 'roles')


class PublisherTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        user = cls._create_user(cls)

        cls.name = 'DC Comics'
        cls.slug = slugify(cls.name)

        cls.publisher = Publisher.objects.create(name=cls.name, slug=cls.slug,
                                                 founded=1934, edited_by=user)

        on_going_series = SeriesType.objects.create(name='Ongoing Series')

        Series.objects.create(name='Superman', slug='superman', sort_name='Superman',
                              series_type=on_going_series, publisher=cls.publisher, volume=1,
                              year_began=1939, edited_by=user)

    def setUp(self):
        self._client_login()

    def test_series_count(self):
        self.assertEqual(self.publisher.series_count, 1)

    def test_publisher_creation(self):
        self.assertTrue(isinstance(self.publisher, Publisher))
        self.assertEqual(str(self.publisher), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.publisher._meta.verbose_name_plural),
                         "publishers")

    def test_absolute_url(self):
        resp = self.client.get(self.publisher.get_absolute_url())
        self.assertEqual(resp.status_code, HTTP_200_OK)


class SeriesTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        user = cls._create_user(cls)

        publisher = Publisher.objects.create(
            name='DC Comics', slug='dc-comics', edited_by=user)
        series_type = SeriesType.objects.create(name='Ongoing Series')
        cls.name = 'Superman'
        cls.superman = Series.objects.create(name=cls.name, slug=slugify(cls.name),
                                             sort_name=cls.name, series_type=series_type,
                                             publisher=publisher, year_began=1939,
                                             edited_by=user)

    def setUp(self):
        self._client_login()

    def test_series_creation(self):
        self.assertTrue(isinstance(self.superman, Series))
        self.assertEqual(str(self.superman), 'Superman (1939)')

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.superman._meta.verbose_name_plural), 'Series')

    def test_absolute_url(self):
        resp = self.client.get(self.superman.get_absolute_url())
        self.assertEqual(resp.status_code, HTTP_200_OK)


class IssueTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        user = cls._create_user(cls)

        issue_date = timezone.now().date()
        publisher = Publisher.objects.create(
            name='DC Comics', slug='dc-comics', edited_by=user)
        series_type = SeriesType.objects.create(name='Ongoing Series')
        cls.series_name = 'Superman'
        cls.superman = Series.objects.create(name=cls.series_name, slug=slugify(cls.series_name),
                                             sort_name=cls.series_name, series_type=series_type,
                                             publisher=publisher, year_began=1939,
                                             edited_by=user)

        cls.issue = Issue.objects.create(series=cls.superman, number='1', slug='superman-1939-1',
                                         cover_date=issue_date, edited_by=user)

    def setUp(self):
        self._client_login()

    def test_issue_creation(self):
        self.assertTrue(isinstance(self.issue, Issue))
        self.assertEqual(str(self.issue), 'Superman #1')

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.issue._meta.verbose_name_plural), 'issues')

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
        cls.name = 'Mini-Series'
        cls.notes = 'A short series typically four issues'

        cls.series_type = SeriesType.objects.create(name=cls.name,
                                                    notes=cls.notes)

    def test_seriestype_creation(self):
        self.assertTrue(isinstance(self.series_type, SeriesType))
        self.assertEqual(str(self.series_type), self.name)
