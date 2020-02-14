import pytest
from django.urls import reverse
from rest_framework import status

from comicsdb.serializers import TeamSerializer


@pytest.mark.django_db
def test_api_team_list_view_accessible_by_name(api_client_with_credentials):
    resp = api_client_with_credentials.get(reverse("api:team-list"))
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_unauthorized_api_team_list_view(api_client):
    resp = api_client.get(reverse("api:team-list"))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_valid_single_team(api_client_with_credentials, team_fixture):
    response = api_client_with_credentials.get(
        reverse("api:team-detail", kwargs={"pk": team_fixture.pk})
    )
    serializer = TeamSerializer(team_fixture)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_invalid_single_team(api_client_with_credentials):
    response = api_client_with_credentials.get(
        reverse("api:team-detail", kwargs={"pk": "10"})
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_unauthorized_api_team_detail_view(api_client, team_fixture):
    response = api_client.get(
        reverse("api:team-detail", kwargs={"pk": team_fixture.pk})
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
