import pytest
from django.contrib.auth.models import Group
from django.utils import timezone

from comicsdb.models.arc import Arc
from comicsdb.models.character import Character
from comicsdb.models.creator import Creator
from comicsdb.models.issue import Issue
from comicsdb.models.publisher import Publisher
from comicsdb.models.series import Series, SeriesType
from users.models import CustomUser


@pytest.fixture
def editor(db):
    grp = Group(user="editor")
    grp.save()
    user = CustomUser.objects.create(username="brian", email="brian@test.com")
    user.set_password("1234")
    user.groups.add(grp)
    user.save()
    return user


@pytest.fixture
def user(db):
    user = CustomUser.objects.create(username="foo", email="foo@bar.com")
    user.set_password("1234")
    user.save()
    return user


@pytest.fixture
def loggedin_user(client, user):
    client.login(username="foo", password="1234")
    return client


@pytest.fixture
def wwh_arc(user):
    return Arc.objects.create(name="World War Hulk", slug="world-war-hulk", edited_by=user)


@pytest.fixture
def fc_arc(user):
    return Arc.objects.create(name="Final Crisis", slug="final-crisis", edited_by=user)


@pytest.fixture
def dc_comics(user):
    return Publisher.objects.create(name="DC Comics", slug="dc-comics", edited_by=user)


@pytest.fixture
def fc_series(user, dc_comics):
    series_type = SeriesType.objects.create(name="Cancelled")
    return Series.objects.create(
        name="Final Crisis",
        slug="final-crisis",
        publisher=dc_comics,
        volume="1",
        year_began=1939,
        series_type=series_type,
        edited_by=user,
    )


@pytest.fixture
def issue_with_arc(user, fc_series, fc_arc):
    i = Issue.objects.create(
        series=fc_series,
        number="1",
        slug="final-crisis-1",
        cover_date=timezone.now().date(),
        edited_by=user,
        created_by=user,
    )
    i.arcs.add(fc_arc)
    return i


@pytest.fixture
def superman(user):
    return Character.objects.create(name="Superman", slug="superman", edited_by=user)


@pytest.fixture
def batman(user):
    return Character.objects.create(name="Batman", slug="batman", edited_by=user)


@pytest.fixture
def john_byrne(user):
    return Creator.objects.create(name="John Byrne", slug="john-byrne", edited_by=user)


@pytest.fixture
def walter_simonson(user):
    return Creator.objects.create(
        name="Walter Simonson", slug="walter-simonson", edited_by=user
    )
