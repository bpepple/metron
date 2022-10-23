from django.urls import reverse
from rest_framework import status

# from comicsdb.models import Publisher
from comicsdb.serializers import SeriesListSerializer


def test_view_url_accessible_by_name(api_client_with_credentials, marvel, dc_comics):
    resp = api_client_with_credentials.get(reverse("api:publisher-list"))
    assert resp.status_code == status.HTTP_200_OK


def test_unauthorized_view_url(api_client, marvel, dc_comics):
    resp = api_client.get(reverse("api:publisher-list"))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


# def test_get_valid_single_publisher(api_client_with_credentials, dc_comics):
#     response = api_client_with_credentials.get(
#         reverse("api:publisher-detail", kwargs={"pk": dc_comics.pk})
#     )
#     publisher = Publisher.objects.get(pk=dc_comics.pk)
#     serializer = PublisherSerializer(publisher)
#     assert response.data == serializer.data
#     assert response.status_code == status.HTTP_200_OK


def test_get_invalid_single_publisher(api_client_with_credentials):
    response = api_client_with_credentials.get(
        reverse("api:publisher-detail", kwargs={"pk": "10"})
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_detail_view_url(api_client, dc_comics):
    response = api_client.get(reverse("api:publisher-detail", kwargs={"pk": dc_comics.pk}))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_publisher_series_list_view(api_client_with_credentials, dc_comics, fc_series):
    resp = api_client_with_credentials.get(
        reverse("api:publisher-series-list", kwargs={"pk": dc_comics.pk})
    )
    serializer = SeriesListSerializer(fc_series)
    assert resp.data["count"] == 1
    assert resp.data["next"] is None
    assert resp.data["previous"] is None
    assert resp.data["results"][0] == serializer.data
    assert resp.status_code == status.HTTP_200_OK
