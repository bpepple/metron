from django.urls import reverse
from rest_framework import status

from comicsdb.models import Team
from comicsdb.serializers import TeamSerializer


def test_view_url_accessible_by_name(api_client_with_credentials, avengers, teen_titans):
    resp = api_client_with_credentials.get(reverse("api:team-list"))
    assert resp.status_code == status.HTTP_200_OK


def test_unauthorized_view_url(api_client, avengers, teen_titans):
    resp = api_client.get(reverse("api:team-list"))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_valid_single_team(api_client_with_credentials, avengers):
    resp = api_client_with_credentials.get(
        reverse("api:team-detail", kwargs={"pk": avengers.pk})
    )
    team = Team.objects.get(pk=avengers.pk)
    serializer = TeamSerializer(team)
    assert resp.data == serializer.data
    assert resp.status_code == status.HTTP_200_OK


def test_get_invalid_single_team(api_client_with_credentials):
    response = api_client_with_credentials.get(reverse("api:team-detail", kwargs={"pk": "10"}))
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_detail_view_url(api_client, avengers):
    response = api_client.get(reverse("api:team-detail", kwargs={"pk": avengers.pk}))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
