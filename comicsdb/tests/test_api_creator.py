from django.urls import reverse
from rest_framework import status

from comicsdb.models import Creator
from comicsdb.serializers import CreatorSerializer


def test_view_url_accessible_by_name(api_client_with_credentials, john_byrne, walter_simonson):
    resp = api_client_with_credentials.get(reverse("api:creator-list"))
    assert resp.status_code == status.HTTP_200_OK


def test_unauthorized_view_url(api_client, john_byrne, walter_simonson):
    resp = api_client.get(reverse("api:creator-list"))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_valid_single_creator(api_client_with_credentials, john_byrne):
    resp = api_client_with_credentials.get(
        reverse("api:creator-detail", kwargs={"pk": john_byrne.pk})
    )
    creator = Creator.objects.get(pk=john_byrne.pk)
    serializer = CreatorSerializer(creator)
    assert resp.data == serializer.data
    assert resp.status_code == status.HTTP_200_OK


def test_get_invalid_single_creator(api_client_with_credentials):
    response = api_client_with_credentials.get(
        reverse("api:creator-detail", kwargs={"pk": "10"})
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_detail_view_url(api_client, john_byrne):
    response = api_client.get(reverse("api:creator-detail", kwargs={"pk": john_byrne.pk}))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
