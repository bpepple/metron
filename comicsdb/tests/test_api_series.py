import pytest
from django.urls import reverse
from rest_framework import status

from comicsdb.serializers import SeriesSerializer


@pytest.mark.django_db
def test_api_series_list_authorized_view(api_client_with_credentials):
    resp = api_client_with_credentials.get(reverse("api:series-list"))
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_api_series_list_unauthorized_view(api_client):
    resp = api_client.get(reverse("api:series-list"))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_authorized_api_series_detail_view(api_client_with_credentials, issue_fixture):
    resp = api_client_with_credentials.get(
        reverse("api:series-detail", kwargs={"pk": issue_fixture.pk})
    )
    serializer = SeriesSerializer(issue_fixture.series)
    assert resp.data == serializer.data
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_unauthorized_api_series_detail_view(api_client, series_fixture):
    response = api_client.get(
        reverse("api:series-detail", kwargs={"pk": series_fixture.pk})
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
