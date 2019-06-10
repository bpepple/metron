from django.urls import reverse
from django.utils import timezone

from comicsdb.models import Issue, Publisher, Series, SeriesType

from .case_base import TestCaseBase

HTML_OK_CODE = 200


class TestWeekView(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        cover_date = timezone.now().date()
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
            series_type=series_type,
            edited_by=user,
        )
        for i_num in range(24):
            Issue.objects.create(
                series=superman,
                number=i_num,
                slug=f"hulk-2019-{i_num}",
                cover_date=cover_date,
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
