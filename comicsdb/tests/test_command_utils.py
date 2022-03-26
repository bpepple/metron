import datetime

from comicsdb.management.commands._utils import (
    determine_cover_date,
    get_week_range_from_store_date,
)


def test_determine_cover_date_marvel():
    result = determine_cover_date(datetime.date(2022, 1, 15), "Marvel Comics")
    expected_result = datetime.date(2022, 3, 1)
    assert result == expected_result


def test_determine_cover_date_other_publisher():
    result = determine_cover_date(datetime.date(2022, 1, 15), "Image")
    expected_result = datetime.date(2022, 1, 1)
    assert result == expected_result


def test_week_range_from_store_date():
    result = get_week_range_from_store_date(datetime.date(2022, 2, 2))
    expected_result = "2022-01-30,2022-02-05"
    assert expected_result == result
