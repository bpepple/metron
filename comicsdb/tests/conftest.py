import uuid

import pytest
from django.utils import timezone

from comicsdb.models.arc import Arc
from comicsdb.models.character import Character
from comicsdb.models.creator import Creator
from comicsdb.models.credits import Role
from comicsdb.models.issue import Issue
from comicsdb.models.publisher import Publisher
from comicsdb.models.series import Series, SeriesType
from comicsdb.models.team import Team
from users.models import CustomUser


@pytest.fixture
def test_password():
    return "strong-test-pass"


@pytest.fixture
def test_email():
    return "foo@bar.com"


@pytest.fixture
def create_user(db, test_password, test_email):
    name = uuid.uuid4()
    user = CustomUser.objects.create(username=name, email=test_email)
    user.set_password(test_password)
    user.save()
    return user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, create_user, api_client):
    api_client.force_authenticate(user=create_user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def wwh_arc(create_user):
    return Arc.objects.create(
        name="World War Hulk", slug="world-war-hulk", edited_by=create_user
    )


@pytest.fixture
def fc_arc(create_user):
    return Arc.objects.create(name="Final Crisis", slug="final-crisis", edited_by=create_user)


@pytest.fixture
def dc_comics(create_user):
    return Publisher.objects.create(name="DC Comics", slug="dc-comics", edited_by=create_user)


@pytest.fixture
def marvel(create_user):
    return Publisher.objects.create(name="Marvel", slug="marvel", edited_by=create_user)


@pytest.fixture
def cancelled_type(db):
    return SeriesType.objects.create(name="Cancelled")


@pytest.fixture
def fc_series(create_user, dc_comics, cancelled_type):
    return Series.objects.create(
        name="Final Crisis",
        slug="final-crisis",
        publisher=dc_comics,
        volume="1",
        year_began=1939,
        series_type=cancelled_type,
        edited_by=create_user,
    )


@pytest.fixture
def issue_with_arc(create_user, fc_series, fc_arc, superman):
    i = Issue.objects.create(
        series=fc_series,
        number="1",
        slug="final-crisis-1",
        cover_date=timezone.now().date(),
        edited_by=create_user,
        created_by=create_user,
    )
    i.arcs.add(fc_arc)
    i.characters.add(superman)
    return i


@pytest.fixture
def superman(create_user):
    return Character.objects.create(name="Superman", slug="superman", edited_by=create_user)


@pytest.fixture
def batman(create_user):
    return Character.objects.create(name="Batman", slug="batman", edited_by=create_user)


@pytest.fixture
def john_byrne(create_user):
    return Creator.objects.create(name="John Byrne", slug="john-byrne", edited_by=create_user)


@pytest.fixture
def walter_simonson(create_user):
    return Creator.objects.create(
        name="Walter Simonson", slug="walter-simonson", edited_by=create_user
    )


@pytest.fixture
def teen_titans(create_user):
    return Team.objects.create(name="Teen Titans", slug="teen-titans", edited_by=create_user)


@pytest.fixture
def avengers(create_user):
    return Team.objects.create(name="The Avengers", slug="the-avengers", edited_by=create_user)


@pytest.fixture
def writer(db):
    return Role.objects.create(name="Writer", notes="Nothing here.", order=20)
