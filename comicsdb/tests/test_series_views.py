from django.test import TestCase
from django.urls import reverse

from comicsdb.models import Publisher, Series, SeriesType
from users.models import CustomUser

HTML_OK_CODE = 200

PAGINATE_TEST_VAL = 35
PAGINATE_DEFAULT_VAL = 28
PAGINATE_DIFF_VAL = (PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL)


class TestCaseBase(TestCase):
    @classmethod
    def _create_user(self):
        user = CustomUser.objects.create(
            username='brian', email='brian@test.com')
        user.set_password('1234')
        user.save()

        return user

    def _client_login(self):
        self.client.login(username='brian', password='1234')


class SeriesSearchViewsTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        cls.publisher = Publisher.objects.create(
            name='DC', slug='dc', edited_by=user)
        series_type = SeriesType.objects.create(name='Ongoing Series')
        for pub_num in range(PAGINATE_TEST_VAL):
            Series.objects.create(name=f'Series {pub_num}',
                                  slug=f'series-{pub_num}',
                                  sort_name=f'Series {pub_num}',
                                  year_began=2018,
                                  publisher=cls.publisher,
                                  series_type=series_type,
                                  edited_by=user)

    def setUp(self):
        self._client_login()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/series/search')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('series:search'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('series:search'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comicsdb/series_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get('/series/search?q=seri')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['series_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_series(self):
        # Get second page and confirm it has (exactly) remaining 5 items
        resp = self.client.get('/series/search?page=2&q=ser')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['series_list']) == PAGINATE_DIFF_VAL)


class SeriesListViewTest(TestCaseBase):

    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        publisher = Publisher.objects.create(
            name='DC', slug='dc', edited_by=user)
        series_type = SeriesType.objects.create(name='Ongoing Series')
        for pub_num in range(PAGINATE_TEST_VAL):
            Series.objects.create(name=f'Series {pub_num}',
                                  slug=f'series-{pub_num}',
                                  sort_name=f'Series {pub_num}',
                                  year_began=2018,
                                  publisher=publisher,
                                  series_type=series_type,
                                  edited_by=user)

    def setUp(self):
        self._client_login()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/series/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('series:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('series:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comicsdb/series_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get(reverse('series:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['series_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_second_page(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get(reverse('series:list') + '?page=2')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['series_list']) == PAGINATE_DIFF_VAL)
