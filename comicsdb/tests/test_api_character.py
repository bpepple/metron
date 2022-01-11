from django.urls import reverse
from rest_framework import status

from comicsdb.models import Character
from comicsdb.serializers import CharacterSerializer


def test_view_url_accessible_by_name(loggedin_user, batman, superman):
    resp = loggedin_user.get(reverse("api:character-list"))
    assert resp.status_code == status.HTTP_200_OK


def test_unauthorized_view_url(client, batman, superman):
    resp = client.get(reverse("api:character-list"))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_valid_single_character(loggedin_user, batman):
    resp = loggedin_user.get(reverse("api:character-detail", kwargs={"pk": batman.pk}))
    character = Character.objects.get(pk=batman.pk)
    serializer = CharacterSerializer(character)
    assert resp.data == serializer.data
    assert resp.status_code == status.HTTP_200_OK


def test_get_invalid_single_character(loggedin_user):
    response = loggedin_user.get(reverse("api:character-detail", kwargs={"pk": "10"}))
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_detail_view_url(client, batman):
    response = client.get(reverse("api:character-detail", kwargs={"pk": batman.pk}))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
