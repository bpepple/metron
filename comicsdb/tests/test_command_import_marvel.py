import datetime

from comicsdb.management.commands.import_marvel import Command
from users.tests.case_base import TestCaseBase


class TestCommandUtils(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        cls.cmd = Command()

    def test_fix_role_wrong_spelling(self):
        res = self.cmd._fix_role("penciler")
        self.assertEqual(res, "penciller")

    def test_fix_role_correct_spelling(self):
        res = self.cmd._fix_role("penciller")
        self.assertEqual(res, "penciller")

    def test_determin_cover_date(self):
        res = self.cmd._determine_cover_date(datetime.date(1999, 11, 30))
        self.assertEqual(res, datetime.date(2000, 1, 1))
