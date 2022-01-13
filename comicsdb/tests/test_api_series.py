from django.urls import reverse
from rest_framework import status

from comicsdb.models import Series
from comicsdb.serializers import SeriesSerializer


def test_view_url_accessible_by_name(api_client_with_credentials):
    resp = api_client_with_credentials.get(reverse("api:series-list"))
    assert resp.status_code == status.HTTP_200_OK


def test_unauthorized_view_url(api_client):
    resp = api_client.get(reverse("api:series-list"))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_valid_single_issue(api_client_with_credentials, fc_series, issue_with_arc):
    resp = api_client_with_credentials.get(
        reverse("api:series-detail", kwargs={"pk": fc_series.pk})
    )
    series = Series.objects.get(pk=fc_series.pk)
    serializer = SeriesSerializer(series)
    assert resp.data == serializer.data
    assert resp.status_code == status.HTTP_200_OK


def test_unauthorized_detail_view_url(api_client, fc_series):
    response = api_client.get(reverse("api:series-detail", kwargs={"pk": fc_series.pk}))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
