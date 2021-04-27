from comicsdb.management.commands.retrieve_weekly_comics import (
    determine_cover_date,
    format_string_to_date,
)
import datetime

from .case_base import TestCaseBase


class YourTestClass(TestCaseBase):
    def test_release_date(self):
        test_str = "2021-04-12"
        expected_result = datetime.date(2021, 4, 12)
        result = format_string_to_date(test_str)
        self.assertEqual(expected_result, result)

    def test_determine_cover_date(self):
        test_date = datetime.date(2021, 4, 12)
        expected_result = datetime.date(2021, 6, 1)

        result = determine_cover_date(test_date)
        self.assertEqual(expected_result, result)
