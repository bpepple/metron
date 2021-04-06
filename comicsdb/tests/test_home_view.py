from comicsdb.models import Issue, Publisher, Series, SeriesType
from django.urls import reverse
from django.utils import timezone

from .case_base import TestCaseBase

HTML_OK_CODE = 200


class HomeViewTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        cover_date = timezone.now().date()
        dc_comics = Publisher.objects.create(name="DC", slug="dc", edited_by=user)
        Publisher.objects.create(name="Marvel", slug="marvel", edited_by=user)
        series_type = SeriesType.objects.create(name="Ongoing Series")
        batman = Series.objects.create(
            name="Batman",
            slug="batman",
            sort_name="Batman",
            year_began=2016,
            publisher=dc_comics,
            volume="1",
            series_type=series_type,
            edited_by=user,
        )
        # Create 10 issues
        for i_num in range(10):
            Issue.objects.create(
                series=batman,
                number=i_num,
                slug=f"batman-2016-{i_num}",
                cover_date=cover_date,
                edited_by=user,
            )

    def setUp(self):
        self._client_login()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("home"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse("home"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, "comicsdb/home.html")
