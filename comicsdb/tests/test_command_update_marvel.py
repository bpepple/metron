from datetime import date

from comicsdb.management.commands.update_marvel import Command
from comicsdb.models.issue import Issue


def test_cleanup_upc():
    test_str = "75960-60592180-0111"
    expected = "75960605921800111"
    result = Command()._cleanup_upc(test_str)
    assert result == expected


def test_bad_query_to_marvel(create_user, fc_series):
    # Test issue that has a non-integer issue number
    user = create_user()
    test_issue = Issue.objects.create(
        series=fc_series,
        number="½",
        slug=f"{fc_series.slug}-0-5",
        cover_date=date(2007, 6, 1),
        edited_by=user,
        created_by=user,
    )
    result = Command()._query_marvel_for_issue(test_issue)
    assert result is None
