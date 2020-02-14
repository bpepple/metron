import pytest
from django.urls import reverse
from rest_framework import status

from comicsdb.serializers import CharacterSerializer


@pytest.mark.django_db
def test_api_character_list_url_accessible_by_name(api_client_with_credentials):
    resp = api_client_with_credentials.get(reverse("api:character-list"))
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_unauthorized_api_character_list(api_client):
    resp = api_client.get(reverse("api:character-list"))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_valid_single_character(api_client_with_credentials, character_fixture):
    response = api_client_with_credentials.get(
        reverse("api:character-detail", kwargs={"pk": character_fixture.pk})
    )
    serializer = CharacterSerializer(character_fixture)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_invalid_single_character(api_client_with_credentials):
    response = api_client_with_credentials.get(
        reverse("api:character-detail", kwargs={"pk": "10"})
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_unauthorized_character_detail_view(api_client, character_fixture):
    response = api_client.get(
        reverse("api:character-detail", kwargs={"pk": character_fixture.pk})
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
