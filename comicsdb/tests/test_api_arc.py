from django.urls import reverse
from rest_framework import status

from comicsdb.models.arc import Arc
from comicsdb.serializers import ArcSerializer, IssueListSerializer


def test_view_url_accessible_by_name(loggedin_user, fc_arc, wwh_arc):
    resp = loggedin_user.get(reverse("api:arc-list"))
    assert resp.status_code == status.HTTP_200_OK


def test_unauthorized_view_url(client, fc_arc, wwh_arc):
    resp = client.get(reverse("api:arc-list"))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_valid_single_arc(loggedin_user, wwh_arc):
    resp = loggedin_user.get(reverse("api:arc-detail", kwargs={"pk": wwh_arc.pk}))
    arc = Arc.objects.get(pk=wwh_arc.pk)
    serializer = ArcSerializer(arc)
    assert resp.data == serializer.data
    assert resp.status_code == status.HTTP_200_OK


def test_get_invalid_single_arc(loggedin_user):
    resp = loggedin_user.get(reverse("api:arc-detail", kwargs={"pk": "10"}))
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_detail_view_url(client, wwh_arc):
    resp = client.get(reverse("api:arc-detail", kwargs={"pk": wwh_arc.pk}))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_arc_issue_list_view(loggedin_user, fc_arc, issue_with_arc):
    resp = loggedin_user.get(reverse("api:arc-issue-list", kwargs={"pk": fc_arc.pk}))
    serializer = IssueListSerializer(issue_with_arc)
    assert resp.data["count"] == 1
    assert resp.data["next"] is None
    assert resp.data["previous"] is None
    assert resp.data["results"][0] == serializer.data
    assert resp.status_code == status.HTTP_200_OK
