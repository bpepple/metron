from django.test import TestCase
from django.urls import reverse

from comicsdb.models import Creator


HTML_OK_CODE = 200

PAGINATE_TEST_VAL = 35
PAGINATE_DEFAULT_VAL = 28
PAGINATE_DIFF_VAL = (PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL)


class CreatorSearchViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for pub_num in range(PAGINATE_TEST_VAL):
            Creator.objects.create(first_name=f'John-{pub_num}',
                                   last_name=f'Smith-{pub_num}',
                                   slug=f'john-smith-{pub_num}')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/creator/search/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('creator:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('creator:search', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comicsdb/creator_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get('/creator/search/page1/?q=smith')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['creator_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_creators(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get('/creator/search/page2/?q=smith')
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['creator_list']) == PAGINATE_DIFF_VAL)


class CreatorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        for pub_num in range(PAGINATE_TEST_VAL):
            Creator.objects.create(first_name=f'John-{pub_num}',
                                   last_name=f'Smith-{pub_num}',
                                   slug=f'john-smith-{pub_num}')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/creator/page1/')
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('creator:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('creator:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, 'comicsdb/creator_list.html')

    def test_pagination_is_thirty(self):
        resp = self.client.get(reverse('creator:list', args=(1,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['creator_list']) == PAGINATE_DEFAULT_VAL)

    def test_lists_second_page(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get(reverse('creator:list', args=(2,)))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(
            len(resp.context['creator_list']) == PAGINATE_DIFF_VAL)
