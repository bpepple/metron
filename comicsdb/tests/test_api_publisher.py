from django.urls import reverse
from rest_framework import status

from comicsdb.models import Publisher
from comicsdb.serializers import PublisherSerializer, SeriesListSerializer


def test_view_url_accessible_by_name(loggedin_user, marvel, dc_comics):
    resp = loggedin_user.get(reverse("api:publisher-list"))
    assert resp.status_code == status.HTTP_200_OK


def test_unauthorized_view_url(client, marvel, dc_comics):
    resp = client.get(reverse("api:publisher-list"))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_valid_single_publisher(loggedin_user, dc_comics):
    response = loggedin_user.get(reverse("api:publisher-detail", kwargs={"pk": dc_comics.pk}))
    publisher = Publisher.objects.get(pk=dc_comics.pk)
    serializer = PublisherSerializer(publisher)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK


def test_get_invalid_single_publisher(loggedin_user):
    response = loggedin_user.get(reverse("api:publisher-detail", kwargs={"pk": "10"}))
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_detail_view_url(client, dc_comics):
    response = client.get(reverse("api:publisher-detail", kwargs={"pk": dc_comics.pk}))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_publisher_series_list_view(loggedin_user, dc_comics, fc_series):
    resp = loggedin_user.get(reverse("api:publisher-series-list", kwargs={"pk": dc_comics.pk}))
    serializer = SeriesListSerializer(fc_series)
    assert resp.data["count"] == 1
    assert resp.data["next"] is None
    assert resp.data["previous"] is None
    assert resp.data["results"][0] == serializer.data
    assert resp.status_code == status.HTTP_200_OK
