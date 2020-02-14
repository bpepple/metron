import pytest
from django.urls import reverse
from rest_framework import status

from comicsdb.serializers import ArcSerializer, IssueListSerializer


@pytest.mark.django_db
def test_api_arc_issue_list(api_client_with_credentials, issue_fixture):
    response = api_client_with_credentials.get(
        reverse("api:arc-issue-list", kwargs={"pk": issue_fixture.pk})
    )
    serializer = IssueListSerializer(issue_fixture)
    assert response.data["count"] == 1
    assert response.data["next"] is None
    assert response.data["previous"] is None
    assert response.data["results"][0] == serializer.data
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_unauthorized_api_arc_detail(api_client, arc_fixture):
    response = api_client.get(reverse("api:arc-detail", kwargs={"pk": arc_fixture.pk}))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_authorized_api_arc_detail(api_client_with_credentials, arc_fixture):
    response = api_client_with_credentials.get(
        reverse("api:arc-detail", kwargs={"pk": arc_fixture.pk})
    )
    serializer = ArcSerializer(arc_fixture)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_invalid_api_arc_detail(api_client_with_credentials, arc_fixture):
    response = api_client_with_credentials.get(
        reverse("api:arc-detail", kwargs={"pk": "10"})
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_authorized_api_arc_list(api_client_with_credentials, arc_fixture):
    response = api_client_with_credentials.get(reverse("api:arc-list"))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_unauthorized_api_arc_list_url(api_client, arc_fixture):
    response = api_client.get(reverse("api:arc-list"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
