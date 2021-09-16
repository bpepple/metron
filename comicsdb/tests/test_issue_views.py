from django.urls import reverse
from django.utils import timezone

from comicsdb.models import Issue, Publisher, Series, SeriesType
from users.tests.case_base import TestCaseBase

HTML_OK_CODE = 200

PAGINATE_TEST_VAL = 35
PAGINATE_DEFAULT_VAL = 28
PAGINATE_DIFF_VAL = PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL


class IssueSearchViewsTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        cover_date = timezone.now().date()
        publisher = Publisher.objects.create(name="DC", slug="dc", edited_by=user)
        series_type = SeriesType.objects.create(name="Ongoing Series")
        superman = Series.objects.create(
            name="Superman",
            slug="superman",
            sort_name="Superman",
            year_began=2018,
            publisher=publisher,
            volume="4",
            series_type=series_type,
            edited_by=user,
        )
        for i_num in range(PAGINATE_TEST_VAL):
            Issue.objects.create(
                series=superman,
                number=i_num,
                slug=f"superman-2018-{i_num}",
                cover_date=cover_date,
                edited_by=user,
                created_by=user,
            )

    def setUp(self):
        self._client_login()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get("/issue/search")
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("issue:search"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse("issue:search"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, "comicsdb/issue_list.html")

    def test_pagination_is_thirty(self):
        resp = self.client.get("/issue/search?q=Super")
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["issue_list"]) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_issues(self):
        # Get second page and confirm it has (exactly) remaining 5 items
        resp = self.client.get("/issue/search?page=2&q=Super")
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["issue_list"]) == PAGINATE_DIFF_VAL)


class IssueListViewTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        cover_date = timezone.now().date()
        publisher = Publisher.objects.create(name="DC", slug="dc", edited_by=user)
        series_type = SeriesType.objects.create(name="Ongoing Series")
        superman = Series.objects.create(
            name="Superman",
            slug="superman",
            sort_name="Superman",
            year_began=2018,
            publisher=publisher,
            volume="4",
            series_type=series_type,
            edited_by=user,
        )
        for i_num in range(PAGINATE_TEST_VAL):
            Issue.objects.create(
                series=superman,
                number=i_num,
                slug=f"superman-2018-{i_num}",
                cover_date=cover_date,
                edited_by=user,
                created_by=user,
            )

    def setUp(self):
        self._client_login()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get("/issue/")
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("issue:list"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse("issue:list"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, "comicsdb/issue_list.html")

    def test_pagination_is_thirty(self):
        resp = self.client.get(reverse("issue:list"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["issue_list"]) == PAGINATE_DEFAULT_VAL)

    def test_lists_second_page(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get(reverse("issue:list") + "?page=2")
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["issue_list"]) == PAGINATE_DIFF_VAL)

    def test_sitemap(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, HTML_OK_CODE)
