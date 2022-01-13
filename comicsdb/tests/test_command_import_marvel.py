import datetime

from comicsdb.management.commands.import_marvel import Command


def test_fix_role_wrong_spelling():
    cmd = Command()
    res = cmd._fix_role("penciler")
    assert res == "penciller"


def test_fix_role_correct_spelling():
    cmd = Command()
    res = cmd._fix_role("penciller")
    assert res == "penciller"


def test_determine_cover_date():
    cmd = Command()
    res = cmd._determine_cover_date(datetime.date(1999, 11, 30))
    assert res == datetime.date(2000, 1, 1)
