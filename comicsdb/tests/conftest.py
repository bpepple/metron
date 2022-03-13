import uuid
from datetime import date, datetime

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

NUMBER_OF_ISSUES = 35


@pytest.fixture
def test_password():
    return "strong-test-pass"


@pytest.fixture
def test_email():
    return "foo@bar.com"


@pytest.fixture
def create_user(db, test_password, test_email):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        kwargs["email"] = test_email
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        return CustomUser.objects.create_user(**kwargs)

    return make_user


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
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def wwh_arc(create_user):
    user = create_user()
    return Arc.objects.create(name="World War Hulk", slug="world-war-hulk", edited_by=user)


@pytest.fixture
def fc_arc(create_user):
    user = create_user()
    return Arc.objects.create(name="Final Crisis", slug="final-crisis", edited_by=user)


@pytest.fixture
def dc_comics(create_user):
    user = create_user()
    return Publisher.objects.create(name="DC Comics", slug="dc-comics", edited_by=user)


@pytest.fixture
def marvel(create_user):
    user = create_user()
    return Publisher.objects.create(name="Marvel", slug="marvel", edited_by=user)


@pytest.fixture
def cancelled_type(db):
    return SeriesType.objects.create(name="Cancelled")


@pytest.fixture
def fc_series(create_user, dc_comics, cancelled_type):
    user = create_user()
    return Series.objects.create(
        name="Final Crisis",
        slug="final-crisis",
        publisher=dc_comics,
        volume="1",
        year_began=1939,
        series_type=cancelled_type,
        edited_by=user,
    )


@pytest.fixture
def issue_with_arc(create_user, fc_series, fc_arc, superman):
    user = create_user()
    i = Issue.objects.create(
        series=fc_series,
        number="1",
        slug="final-crisis-1",
        cover_date=timezone.now().date(),
        edited_by=user,
        created_by=user,
    )
    i.arcs.add(fc_arc)
    i.characters.add(superman)
    return i


@pytest.fixture
def list_of_issues(create_user, fc_series):
    user = create_user()

    # Create the store date for this week
    year, week, _ = date.today().isocalendar()
    # The "3" is the weekday (Wednesday)
    wednesday = f"{year}-{week}-3"
    # Dates used in Issue creating
    in_store_date = datetime.strptime(wednesday, "%G-%V-%u")
    cover_date = date.today()

    for i_num in range(NUMBER_OF_ISSUES):
        Issue.objects.create(
            series=fc_series,
            number=i_num,
            slug=f"final-crisis-1939-{i_num}",
            cover_date=cover_date,
            store_date=in_store_date,
            edited_by=user,
            created_by=user,
        )


@pytest.fixture
def superman(create_user):
    user = create_user()
    return Character.objects.create(name="Superman", slug="superman", edited_by=user)


@pytest.fixture
def batman(create_user):
    user = create_user()
    return Character.objects.create(name="Batman", slug="batman", edited_by=user)


@pytest.fixture
def john_byrne(create_user):
    user = create_user()
    return Creator.objects.create(name="John Byrne", slug="john-byrne", edited_by=user)


@pytest.fixture
def walter_simonson(create_user):
    user = create_user()
    return Creator.objects.create(
        name="Walter Simonson", slug="walter-simonson", edited_by=user
    )


@pytest.fixture
def teen_titans(create_user):
    user = create_user()
    return Team.objects.create(name="Teen Titans", slug="teen-titans", edited_by=user)


@pytest.fixture
def avengers(create_user):
    user = create_user()
    return Team.objects.create(name="The Avengers", slug="the-avengers", edited_by=user)


@pytest.fixture
def writer(db):
    return Role.objects.create(name="Writer", notes="Nothing here.", order=20)
