import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from comicsdb.models import Team

HTML_OK_CODE = 200

PAGINATE_TEST_VAL = 35
PAGINATE_DEFAULT_VAL = 28
PAGINATE_DIFF_VAL = PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL


@pytest.fixture
def list_of_series(create_user):
    user = create_user()
    for pub_num in range(PAGINATE_TEST_VAL):
        Team.objects.create(name=f"Team {pub_num}", slug=f"team-{pub_num}", edited_by=user)


def test_team_search_view_url_exists_at_desired_location(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get("/team/search")
    assert resp.status_code == HTML_OK_CODE


def test_team_search_view_url_accessible_by_name(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get(reverse("team:search"))
    assert resp.status_code == HTML_OK_CODE


def test_team_search_view_uses_correct_template(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get(reverse("team:search"))
    assert resp.status_code == HTML_OK_CODE
    assertTemplateUsed(resp, "comicsdb/team_list.html")


def test_team_search_pagination_is_thirty(auto_login_user, list_of_series):
    client, _ = auto_login_user()
    resp = client.get("/team/search?q=tea")
    assert resp.status_code == HTML_OK_CODE
    assert "is_paginated" in resp.context
    assert resp.context["is_paginated"] is True
    assert len(resp.context["team_list"]) == PAGINATE_DEFAULT_VAL


def test_team_search_lists_all_teams(auto_login_user, list_of_series):
    # Get second page and confirm it has (exactly) remaining 7 items
    client, _ = auto_login_user()
    resp = client.get("/team/search?page=2&q=tea")
    assert resp.status_code == HTML_OK_CODE
    assert "is_paginated" in resp.context
    assert resp.context["is_paginated"] is True
    assert len(resp.context["team_list"]) == PAGINATE_DIFF_VAL


def test_team_list_view_url_exists_at_desired_location(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get("/team/")
    assert resp.status_code == HTML_OK_CODE


def test_team_list_view_url_accessible_by_name(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get(reverse("team:list"))
    assert resp.status_code == HTML_OK_CODE


def test_team_list_view_uses_correct_template(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get(reverse("team:list"))
    assert resp.status_code == HTML_OK_CODE
    assertTemplateUsed(resp, "comicsdb/team_list.html")


def test_team_list_pagination_is_thirty(auto_login_user, list_of_series):
    client, _ = auto_login_user()
    resp = client.get(reverse("team:list"))
    assert resp.status_code == HTML_OK_CODE
    assert "is_paginated" in resp.context
    assert resp.context["is_paginated"] is True
    assert len(resp.context["team_list"]) == PAGINATE_DEFAULT_VAL


def test_team_lists_second_page(auto_login_user, list_of_series):
    # Get second page and confirm it has (exactly) remaining 7 items
    client, _ = auto_login_user()
    resp = client.get(reverse("team:list") + "?page=2")
    assert resp.status_code == HTML_OK_CODE
    assert "is_paginated" in resp.context
    assert resp.context["is_paginated"] is True
    assert len(resp.context["team_list"]) == PAGINATE_DIFF_VAL
