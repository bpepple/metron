from django.test import TestCase
from django.urls import reverse

from comicsdb.models import Series, Publisher, SeriesType


HTML_OK_CODE = 200

PAGINATE_TEST_VAL = 35
PAGINATE_DEFAULT_VAL = 28
PAGINATE_DIFF_VAL = (PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL)


class SeriesSearchViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.publisher = Publisher.objects.create(name='DC', slug='dc')
        series_type = SeriesType.objects.create(name='Ongoing Series')
        for pub_num in range(PAGINATE_TEST_VAL):
            Series.objects.create(name=f'Series {pub_num}',
                                  slug=f'series-{pub_num}',
                                  sort_name=f'Series {pub_num}',
                                  year_began=2018,
                                  publisher=cls.publisher,
                                  series_type=series_type)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/series/search/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('series:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('series:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comicsdb/series_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get('/series/search/page1/?q=seri')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['series_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_series(self):
        # Get second page and confirm it has (exactly) remaining 5 items
        resp = self.client.get('/series/search/page2/?q=ser')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['series_list']) == PAGINATE_DIFF_VAL)


class SeriesListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        publisher = Publisher.objects.create(name='DC', slug='dc')
        series_type = SeriesType.objects.create(name='Ongoing Series')
        for pub_num in range(PAGINATE_TEST_VAL):
            Series.objects.create(name=f'Series {pub_num}',
                                  slug=f'series-{pub_num}',
                                  sort_name=f'Series {pub_num}',
                                  year_began=2018,
                                  publisher=publisher,
                                  series_type=series_type)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/series/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('series:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('series:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comicsdb/series_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get(reverse('series:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['series_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_second_page(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get(reverse('series:list', args=(2,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['series_list']) == PAGINATE_DIFF_VAL)
