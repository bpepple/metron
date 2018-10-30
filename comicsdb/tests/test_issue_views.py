from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from comicsdb.models import Series, Publisher, SeriesType, Issue


HTML_OK_CODE = 200

PAGINATE_TEST_VAL = 35
PAGINATE_DEFAULT_VAL = 30
PAGINATE_DIFF_VAL = (PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL)


class IssueSearchViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cover_date = issue_date = timezone.now().date()
        publisher = Publisher.objects.create(name='DC', slug='dc')
        series_type = SeriesType.objects.create(name='Ongoing Series')
        superman = Series.objects.create(name='Superman', slug='superman',
                                         sort_name='Superman', year_began=2018,
                                         publisher=publisher, series_type=series_type)
        for i_num in range(PAGINATE_TEST_VAL):
            Issue.objects.create(series=superman, number=i_num,
                                 slug=f'superman-2018-{i_num}', cover_date=cover_date)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/issue/search/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('issue:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('issue:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comicsdb/issue_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get('/issue/search/page1/?q=super')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['issue_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_series(self):
        # Get second page and confirm it has (exactly) remaining 5 items
        resp = self.client.get('/issue/search/page2/?q=super')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['issue_list']) == PAGINATE_DIFF_VAL)


class IssueListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cover_date = issue_date = timezone.now().date()
        publisher = Publisher.objects.create(name='DC', slug='dc')
        series_type = SeriesType.objects.create(name='Ongoing Series')
        superman = Series.objects.create(name='Superman', slug='superman',
                                         sort_name='Superman', year_began=2018,
                                         publisher=publisher, series_type=series_type)
        for i_num in range(PAGINATE_TEST_VAL):
            Issue.objects.create(series=superman, number=i_num,
                                 slug=f'superman-2018-{i_num}', cover_date=cover_date)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/issue/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('issue:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('issue:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comicsdb/issue_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get(reverse('issue:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['issue_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_second_page(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get(reverse('issue:list', args=(2,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['issue_list']) == PAGINATE_DIFF_VAL)
