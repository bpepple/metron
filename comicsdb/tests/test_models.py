from comicsdb.models import (
    Arc,
    Character,
    Creator,
    Issue,
    Publisher,
    Role,
    Series,
    SeriesType,
    Team,
)

HTTP_200_OK = 200


def test_team_creation(avengers):
    assert isinstance(avengers, Team)
    assert str(avengers) == avengers.name


def test_team_verbose_name_plural(avengers):
    assert str(avengers._meta.verbose_name_plural) == "teams"


def test_team_absolute_url(client, avengers):
    resp = client.get(avengers.get_absolute_url())
    assert resp.status_code == HTTP_200_OK


def test_character_creation(batman):
    assert isinstance(batman, Character)
    assert str(batman) == batman.name


def test_character_verbose_name_plural(batman):
    assert str(batman._meta.verbose_name_plural) == "characters"


def test_character_absolute_url(client, batman):
    resp = client.get(batman.get_absolute_url())
    assert resp.status_code == HTTP_200_OK


def test_arc_creation(wwh_arc):
    assert isinstance(wwh_arc, Arc)
    assert str(wwh_arc) == wwh_arc.name


def test_arc_verbose_name_plural(wwh_arc):
    assert str(wwh_arc._meta.verbose_name_plural) == "arcs"


def test_arc_absolute_url(client, wwh_arc):
    resp = client.get(wwh_arc.get_absolute_url())
    assert resp.status_code == HTTP_200_OK


def test_creator_creation(john_byrne):
    assert isinstance(john_byrne, Creator)
    assert str(john_byrne) == john_byrne.name


def test_creator_get_full_name(john_byrne):
    assert john_byrne.name == john_byrne.name


def test_creator_verbose_name_plural(john_byrne):
    assert str(john_byrne._meta.verbose_name_plural) == "creators"


def test_creator_absolute_url(client, john_byrne):
    resp = client.get(john_byrne.get_absolute_url())
    assert resp.status_code == HTTP_200_OK


def test_role_creation(writer):
    assert isinstance(writer, Role)
    assert str(writer) == writer.name


def test_role_verbose_name_plural(writer):
    assert str(writer._meta.verbose_name_plural) == "roles"


def test_publisher_series_count(dc_comics, fc_series):
    assert dc_comics.series_count == 1


def test_publisher_creation(dc_comics):
    assert isinstance(dc_comics, Publisher)
    assert str(dc_comics) == dc_comics.name


def test_publisher_verbose_name_plural(dc_comics):
    assert str(dc_comics._meta.verbose_name_plural) == "publishers"


def test_puiblisher_absolute_url(client, dc_comics):
    resp = client.get(dc_comics.get_absolute_url())
    assert resp.status_code == HTTP_200_OK


def test_series_creation(fc_series):
    assert isinstance(fc_series, Series)
    assert str(fc_series), "Final Crisis (1939)"


def test_series_verbose_name_plural(fc_series):
    assert str(fc_series._meta.verbose_name_plural) == "Series"


def test_series_absolute_url(client, fc_series):
    resp = client.get(fc_series.get_absolute_url())
    assert resp.status_code == HTTP_200_OK


def test_issue_creation(issue_with_arc):
    assert isinstance(issue_with_arc, Issue)
    assert str(issue_with_arc) == "Final Crisis (1939) #1"


def test_issue_verbose_name_plural(issue_with_arc):
    assert str(issue_with_arc._meta.verbose_name_plural) == "issues"


def test_issue_absolute_url(client, issue_with_arc):
    resp = client.get(issue_with_arc.get_absolute_url())
    assert resp.status_code == HTTP_200_OK


# This test should be in the SeriesTest but for now let's leave this here.
def test_issue_count(issue_with_arc, superman):
    issue_count = superman.issue_count
    assert issue_count == 1


def test_seriestype_creation(cancelled_type):
    assert isinstance(cancelled_type, SeriesType)
    assert str(cancelled_type) == cancelled_type.name
