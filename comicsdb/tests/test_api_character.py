from typing import Any

import pytest
from django.urls import reverse
from rest_framework import status

from comicsdb.models.creator import Creator
from comicsdb.models.team import Team


@pytest.fixture
def create_character_data(john_byrne: Creator, teen_titans: Team) -> dict[str, Any]:
    return {
        "name": "Wolverine",
        "desc": "Blah Blah",
        "alias": [
            "Wolvie",
        ],
        "creators": [john_byrne.id],
        "teams": [teen_titans.id],
    }


@pytest.fixture
def create_put_data():
    return {"desc": "The Dark Knight", "alias": ["Bruce Wayne"]}


# Post Tests
def test_unauthorized_post_url(db, api_client, create_character_data):
    resp = api_client.post(reverse("api:character-list"), data=create_character_data)
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_post_url(api_client_with_credentials, create_character_data):
    resp = api_client_with_credentials.post(
        reverse("api:character-list"), data=create_character_data
    )
    assert resp.status_code == status.HTTP_403_FORBIDDEN


# Put Tests
def test_unauthorized_put_url(db, api_client, batman, create_put_data):
    resp = api_client.put(
        reverse("api:character-detail", kwargs={"pk": batman.pk}), data=create_put_data
    )
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_put_url(api_client_with_credentials, batman, create_put_data):
    resp = api_client_with_credentials.put(
        reverse("api:character-detail", kwargs={"pk": batman.pk}), data=create_put_data
    )
    assert resp.status_code == status.HTTP_403_FORBIDDEN


def test_staff_user_put_url(api_client_with_staff_credentials, batman, create_put_data):
    resp = api_client_with_staff_credentials.patch(
        reverse("api:character-detail", kwargs={"pk": batman.pk}), data=create_put_data
    )
    assert resp.status_code == status.HTTP_200_OK


# Regular Tests
def test_admin_user_post_url(db, api_client_with_staff_credentials, create_character_data):
    resp = api_client_with_staff_credentials.post(
        reverse("api:character-list"), data=create_character_data
    )
    assert resp.status_code == status.HTTP_201_CREATED


def test_view_url_accessible_by_name(api_client_with_credentials, batman, superman):
    resp = api_client_with_credentials.get(reverse("api:character-list"))
    assert resp.status_code == status.HTTP_200_OK


def test_unauthorized_view_url(api_client, batman, superman):
    resp = api_client.get(reverse("api:character-list"))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_valid_single_character(api_client_with_credentials, batman):
    resp = api_client_with_credentials.get(
        reverse("api:character-detail", kwargs={"pk": batman.pk})
    )
    assert resp.status_code == status.HTTP_200_OK


def test_get_invalid_single_character(api_client_with_credentials):
    response = api_client_with_credentials.get(
        reverse("api:character-detail", kwargs={"pk": "10"})
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_detail_view_url(api_client, batman):
    response = api_client.get(reverse("api:character-detail", kwargs={"pk": batman.pk}))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
