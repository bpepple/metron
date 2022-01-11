from django.urls import reverse
from rest_framework import status

from comicsdb.models import Creator
from comicsdb.serializers import CreatorSerializer


def test_view_url_accessible_by_name(loggedin_user, john_byrne, walter_simonson):
    resp = loggedin_user.get(reverse("api:creator-list"))
    assert resp.status_code == status.HTTP_200_OK


def test_unauthorized_view_url(client, john_byrne, walter_simonson):
    resp = client.get(reverse("api:creator-list"))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_valid_single_creator(loggedin_user, john_byrne):
    resp = loggedin_user.get(reverse("api:creator-detail", kwargs={"pk": john_byrne.pk}))
    creator = Creator.objects.get(pk=john_byrne.pk)
    serializer = CreatorSerializer(creator)
    assert resp.data == serializer.data
    assert resp.status_code == status.HTTP_200_OK


def test_get_invalid_single_creator(loggedin_user):
    response = loggedin_user.get(reverse("api:creator-detail", kwargs={"pk": "10"}))
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_detail_view_url(client, john_byrne):
    response = client.get(reverse("api:creator-detail", kwargs={"pk": john_byrne.pk}))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
