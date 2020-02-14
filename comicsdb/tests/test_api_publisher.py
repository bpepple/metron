import pytest
from django.urls import reverse
from rest_framework import status

from comicsdb.serializers import PublisherSerializer, SeriesListSerializer


@pytest.mark.django_db
def test_view_url_accessible_by_name(api_client_with_credentials):
    response = api_client_with_credentials.get(reverse("api:publisher-list"))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_unauthorized_view_url(api_client):
    response = api_client.get(reverse("api:publisher-list"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_valid_single_publisher(api_client_with_credentials, publisher_fixture):
    response = api_client_with_credentials.get(
        reverse("api:publisher-detail", kwargs={"pk": publisher_fixture.pk})
    )

    serializer = PublisherSerializer(publisher_fixture)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_invalid_single_publisher(api_client_with_credentials):
    response = api_client_with_credentials.get(
        reverse("api:publisher-detail", kwargs={"pk": "10"})
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_unauthorized_api_detail_view(api_client, publisher_fixture):

    response = api_client.get(
        reverse("api:publisher-detail", kwargs={"pk": publisher_fixture.pk})
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_publisher_series_list_view(api_client_with_credentials, series_fixture):
    response = api_client_with_credentials.get(
        reverse("api:publisher-series-list", kwargs={"pk": series_fixture.publisher.pk})
    )
    serializer = SeriesListSerializer(series_fixture)
    assert response.data["count"] == 1
    assert response.data["next"] is None
    assert response.data["previous"] is None
    assert response.data["results"][0] == serializer.data
    assert response.status_code == status.HTTP_200_OK
