import datetime

from comicsdb.management.commands._utils import get_week_range_from_store_date


def test_week_range_from_store_date():
    result = get_week_range_from_store_date(datetime.date(2022, 2, 2))
    expected_result = "2022-01-30,2022-02-05"
    assert expected_result == result
