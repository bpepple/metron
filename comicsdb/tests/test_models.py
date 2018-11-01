from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from comicsdb.models import (Publisher, Series, SeriesType,
                             Creator, Role, Issue)


HTTP_200_OK = 200


class CreatorTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.first_name = 'Walter'
        cls.last_name = 'Simonson'
        cls.full_name = f'{cls.first_name} {cls.last_name}'
        cls.slug = 'walter-simonson'
        cls.creator = Creator.objects.create(first_name=cls.first_name,
                                             last_name=cls.last_name,
                                             slug=cls.slug)

    def test_creator_creation(self):
        self.assertTrue(isinstance(self.creator, Creator))
        self.assertEqual(str(self.creator), self.full_name)

    def test_creator_get_full_name(self):
        self.assertEqual(self.creator.get_full_name(), self.full_name)

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
        cls.role = Role.objects.create(name=cls.name, notes=notes)

    def test_role_creation(self):
        self.assertTrue(isinstance(self.role, Role))
        self.assertEqual(str(self.role), self.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.role._meta.verbose_name_plural), 'roles')


class PublisherTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.name = 'DC Comics'
        cls.slug = slugify(cls.name)
        cls.short_desc = 'Home of Superman'

        cls.publisher = Publisher.objects.create(name=cls.name, slug=cls.slug,
                                                 short_desc=cls.short_desc, founded=1934)

        on_going_series = SeriesType.objects.create(name='Ongoing Series')

        Series.objects.create(name='Superman', slug='superman', sort_name='Superman',
                              series_type=on_going_series, publisher=cls.publisher, volume=1,
                              year_began=1939, short_desc='The one that started it all.')

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


class SeriesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        publisher = Publisher.objects.create(
            name='DC Comics', slug='dc-comics')
        series_type = SeriesType.objects.create(name='Ongoing Series')
        cls.name = 'Superman'
        cls.superman = Series.objects.create(name=cls.name, slug=slugify(cls.name),
                                             sort_name=cls.name, series_type=series_type,
                                             publisher=publisher, year_began=1939)

    def test_series_creation(self):
        self.assertTrue(isinstance(self.superman, Series))
        self.assertEqual(str(self.superman), 'Superman (1939)')

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(self.superman._meta.verbose_name_plural), 'Series')

    def test_absolute_url(self):
        resp = self.client.get(self.superman.get_absolute_url())
        self.assertEqual(resp.status_code, HTTP_200_OK)


class IssueTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        issue_date = timezone.now().date()
        publisher = Publisher.objects.create(
            name='DC Comics', slug='dc-comics')
        series_type = SeriesType.objects.create(name='Ongoing Series')
        cls.series_name = 'Superman'
        cls.superman = Series.objects.create(name=cls.series_name, slug=slugify(cls.series_name),
                                             sort_name=cls.series_name, series_type=series_type,
                                             publisher=publisher, year_began=1939)

        cls.issue = Issue.objects.create(series=cls.superman, number='1', slug='superman-1939-1',
                                         cover_date=issue_date)

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
