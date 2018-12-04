from django.test import TestCase
from django.urls import reverse

from comicsdb.models import Arc


HTML_OK_CODE = 200

PAGINATE_TEST_VAL = 35
PAGINATE_DEFAULT_VAL = 28
PAGINATE_DIFF_VAL = (PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL)


class ArcSearchViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for pub_num in range(PAGINATE_TEST_VAL):
            Arc.objects.create(name='Arc %s' % pub_num,
                               slug='arc-%s' % pub_num)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/arc/search')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('arc:search'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('arc:search'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comicsdb/arc_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get('/arc/search?q=arc')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['arc_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_arcs(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get('/arc/search?page=2&q=arc')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['arc_list']) == PAGINATE_DIFF_VAL)


class ArcListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        for pub_num in range(PAGINATE_TEST_VAL):
            Arc.objects.create(
                name='Arc %s' % pub_num,
                slug='arc-%s' % pub_num)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/arc/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('arc:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('arc:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comicsdb/arc_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get(reverse('arc:list'))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['arc_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_second_page(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get(reverse('arc:list') + '?page=2')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['arc_list']) == PAGINATE_DIFF_VAL)
