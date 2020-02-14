import pytest
from django.urls import reverse
from rest_framework import status

from comicsdb.serializers import CreatorSerializer


@pytest.mark.django_db
def test_authorize_creator_api_view(api_client_with_credentials):
    resp = api_client_with_credentials.get(reverse("api:creator-list"))
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_unauthorized_creator_api_view(api_client):
    resp = api_client.get(reverse("api:creator-list"))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_valid_single_creator(api_client_with_credentials, creator_fixture):
    response = api_client_with_credentials.get(
        reverse("api:creator-detail", kwargs={"pk": creator_fixture.pk})
    )
    serializer = CreatorSerializer(creator_fixture)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_invalid_single_creator(api_client_with_credentials):
    response = api_client_with_credentials.get(
        reverse("api:creator-detail", kwargs={"pk": "10"})
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_unauthorized_view_url(api_client, creator_fixture):
    response = api_client.get(
        reverse("api:creator-detail", kwargs={"pk": creator_fixture.pk})
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
