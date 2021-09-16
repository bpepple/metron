import datetime

from comicsdb.management.commands.import_shortboxed import determine_cover_date
from users.tests.case_base import TestCaseBase


class TestSandBoxedCommands(TestCaseBase):
    def test_determine_marvel_cover_date(self):
        test_date = datetime.date(2021, 4, 12)
        expected_result = datetime.date(2021, 6, 1)
        result = determine_cover_date(test_date, "marvel comics")
        self.assertEqual(expected_result, result)

    def test_determine_image_cover_date(self):
        test_date = datetime.date(2021, 4, 12)
        expected_result = datetime.date(2021, 4, 1)
        result = determine_cover_date(test_date, "IMAGE COMICS")
        self.assertEqual(expected_result, result)
