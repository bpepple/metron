import uuid

import pytest
from django.utils import timezone

from comicsdb.models import (
    Arc,
    Character,
    Creator,
    Issue,
    Publisher,
    Series,
    SeriesType,
    Team,
)
from users.models import CustomUser


@pytest.fixture
def test_password():
    return "strong*test#pass12345"


@pytest.fixture
def test_email():
    return "test@example.com"


@pytest.fixture
def create_user(db, test_password, test_email):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        if "email" not in kwargs:
            kwargs["email"] = test_email
        return CustomUser.objects.create(**kwargs)

    return make_user


@pytest.fixture()
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
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def arc_fixture(db, create_user):
    user = create_user()
    return Arc.objects.create(
        name="World War Hulk", slug="world-war-hulk", edited_by=user
    )


@pytest.fixture
def creator_fixture(db, create_user):
    user = create_user()
    return Creator.objects.create(
        name="Walter Simonson", slug="walter-simonson", edited_by=user
    )


@pytest.fixture
def character_fixture(db, create_user):
    user = create_user()
    return Character.objects.create(name="Superman", slug="superman", edited_by=user)


@pytest.fixture
def publisher_fixture(db, create_user):
    user = create_user()
    return Publisher.objects.create(name="DC Comics", slug="dc-comics", edited_by=user)


@pytest.fixture
def team_fixture(db, create_user):
    user = create_user()
    return Team.objects.create(name="Teen Titans", slug="teen-titans", edited_by=user)


@pytest.fixture
def series_fixture(db, create_user, publisher_fixture):
    user = create_user()
    series_type = SeriesType.objects.create(name="Cancelled")
    return Series.objects.create(
        name="Final Crisis",
        slug="final-crisis",
        publisher=publisher_fixture,
        volume="1",
        year_began=1999,
        series_type=series_type,
        edited_by=user,
    )


@pytest.fixture
def issue_fixture(db, create_user, series_fixture):
    user = create_user()
    arc = Arc.objects.create(name="Final Crisis", slug="final-crisis", edited_by=user)
    issue = Issue.objects.create(
        series=series_fixture,
        number="1",
        slug="final-crisis-1",
        cover_date=timezone.now().date(),
        edited_by=user,
    )
    issue.arcs.add(arc)
    return issue
