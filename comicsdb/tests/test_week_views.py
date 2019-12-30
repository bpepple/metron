from datetime import date, datetime

from django.urls import reverse

from comicsdb.models import Issue, Publisher, Series, SeriesType

from .case_base import TestCaseBase

HTML_OK_CODE = 200

PAGINATE_TEST_VAL = 35
PAGINATE_DEFAULT_VAL = 28
PAGINATE_DIFF_VAL = PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL


class TestWeekView(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        # Create the store date for this week
        year, week, _ = date.today().isocalendar()
        # The "3" is the weekday (Wednesday)
        wednesday = f"{year}-{week}-3"
        # Dates used in Issue creating
        in_store_date = datetime.strptime(wednesday, "%G-%V-%u")
        cover_date = date.today()

        user = cls._create_user()

        publisher = Publisher.objects.create(
            name="Marvel", slug="marvel", edited_by=user
        )
        series_type = SeriesType.objects.create(name="Ongoing Series")
        superman = Series.objects.create(
            name="Hukj",
            slug="hulk",
            sort_name="hulk",
            year_began=2018,
            publisher=publisher,
            volume=3,
            series_type=series_type,
            edited_by=user,
        )
        for i_num in range(PAGINATE_TEST_VAL):
            Issue.objects.create(
                series=superman,
                number=i_num,
                slug=f"hulk-2019-{i_num}",
                cover_date=cover_date,
                store_date=in_store_date,
                edited_by=user,
            )

    def setUp(self):
        self._client_login()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get("/week/")
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("week:list"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse("week:list"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, "comicsdb/week_list.html")

    def test_pagination_is_thirty(self):
        resp = self.client.get(reverse("week:list"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["issue_list"]) == PAGINATE_DEFAULT_VAL)

    def test_lists_second_page(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get(reverse("week:list") + "?page=2")
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["issue_list"]) == PAGINATE_DIFF_VAL)
