from django.urls import reverse
from rest_framework import status

from comicsdb.models import Character
from comicsdb.serializers import CharacterSerializer


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
    character = Character.objects.get(pk=batman.pk)
    serializer = CharacterSerializer(character)
    assert resp.data == serializer.data
    assert resp.status_code == status.HTTP_200_OK


def test_get_invalid_single_character(api_client_with_credentials):
    response = api_client_with_credentials.get(
        reverse("api:character-detail", kwargs={"pk": "10"})
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_detail_view_url(api_client, batman):
    response = api_client.get(reverse("api:character-detail", kwargs={"pk": batman.pk}))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
