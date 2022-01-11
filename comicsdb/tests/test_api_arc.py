import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from comicsdb.models import Arc, Issue, Publisher, Series, SeriesType
from comicsdb.serializers import ArcSerializer, IssueListSerializer


@pytest.fixture
def wwh_arc(user):
    return Arc.objects.create(name="World War Hulk", slug="world-war-hulk", edited_by=user)


@pytest.fixture
def fc_arc(user):
    return Arc.objects.create(name="Final Crisis", slug="final-crisis", edited_by=user)


@pytest.fixture
def dc_comics(user):
    return Publisher.objects.create(name="DC Comics", slug="dc-comics", edited_by=user)


@pytest.fixture
def final_crisis(user, dc_comics):
    series_type = SeriesType.objects.create(name="Cancelled")
    return Series.objects.create(
        name="Final Crisis",
        slug="final-crisis",
        publisher=dc_comics,
        volume="1",
        year_began=1939,
        series_type=series_type,
        edited_by=user,
    )


@pytest.fixture
def arc_issue(user, final_crisis, fc_arc):
    i = Issue.objects.create(
        series=final_crisis,
        number="1",
        slug="final-crisis-1",
        cover_date=timezone.now().date(),
        edited_by=user,
        created_by=user,
    )
    i.arcs.add(fc_arc)
    return i


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


def test_arc_issue_list_view(loggedin_user, fc_arc, arc_issue):
    resp = loggedin_user.get(reverse("api:arc-issue-list", kwargs={"pk": fc_arc.pk}))
    serializer = IssueListSerializer(arc_issue)
    assert resp.data["count"] == 1
    assert resp.data["next"] is None
    assert resp.data["previous"] is None
    assert resp.data["results"][0] == serializer.data
    assert resp.status_code == status.HTTP_200_OK
