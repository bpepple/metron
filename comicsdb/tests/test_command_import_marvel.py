import datetime

from django.utils import timezone

from comicsdb.management.commands.import_marvel import Command
from comicsdb.models import Creator, Credits, Issue, Publisher, Role, Series, SeriesType
from users.tests.case_base import TestCaseBase


class TestCommandUtils(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        cls.cmd = Command()

        user = cls._create_user()

        cover_date = timezone.now().date()
        publisher_obj = Publisher.objects.create(name="Foo", slug="foo", edited_by=user)
        series_type_obj = SeriesType.objects.create(name="Blah Blah")
        special_man = Series.objects.create(
            name="Specialman",
            slug="specialman",
            publisher=publisher_obj,
            volume="1",
            year_began=2020,
            series_type=series_type_obj,
            edited_by=user,
        )
        cls.issue = Issue.objects.create(
            series=special_man,
            number="5",
            slug=f"specialman-2020-{5}",
            cover_date=cover_date,
            edited_by=user,
            created_by=user,
        )
        cls.cb = Creator.objects.create(
            name="C.B. Cebulski", slug="c-b-cebulski", edited_by=user
        )
        Role.objects.create(name="Editor in Chief", order=150)

    def setUp(self):
        self._client_login()

    def test_fix_role_wrong_spelling(self):
        res = self.cmd._fix_role("penciler")
        self.assertEqual(res, "penciller")

    def test_fix_role_correct_spelling(self):
        res = self.cmd._fix_role("penciller")
        self.assertEqual(res, "penciller")

    def test_determin_cover_date(self):
        res = self.cmd._determine_cover_date(datetime.date(1999, 11, 30))
        self.assertEqual(res, datetime.date(2000, 1, 1))

    def test_add_eic(self):
        self.cmd._add_eic_credit(self.issue)
        res = Credits.objects.get(creator=self.cb, issue=self.issue)
        self.assertIsInstance(res, Credits)
        self.assertEqual(res.creator, self.cb)
