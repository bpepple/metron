from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

HTML_OK_CODE = 200

PAGINATE_TEST_VAL = 35
PAGINATE_DEFAULT_VAL = 28
PAGINATE_DIFF_VAL = PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL


# This week tests
def test_view_url_exists_at_desired_location(db, client):
    resp = client.get("/issue/thisweek")
    assert resp.status_code == HTML_OK_CODE


def test_view_url_accessible_by_name(db, client):
    resp = client.get(reverse("issue:thisweek"))
    assert resp.status_code == HTML_OK_CODE


def test_view_uses_correct_template(db, client):
    resp = client.get(reverse("issue:thisweek"))
    assert resp.status_code == HTML_OK_CODE
    assertTemplateUsed(resp, "comicsdb/week_list.html")


def test_pagination_is_thirty(db, client, list_of_issues):
    resp = client.get(reverse("issue:thisweek"))
    assert resp.status_code == HTML_OK_CODE
    assert "is_paginated" in resp.context
    assert resp.context["is_paginated"] is True
    assert len(resp.context["issue_list"]) == PAGINATE_DEFAULT_VAL


def test_lists_second_page(db, client, list_of_issues):
    # Get second page and confirm it has (exactly) remaining 7 items
    resp = client.get(reverse("issue:thisweek") + "?page=2")
    assert resp.status_code == HTML_OK_CODE
    assert "is_paginated" in resp.context
    assert resp.context["is_paginated"] is True
    assert len(resp.context["issue_list"]) == PAGINATE_DIFF_VAL


# Next week tests
def test_nextweek_view_url_exists_at_desired_location(db, client):
    resp = client.get("/issue/nextweek")
    assert resp.status_code == HTML_OK_CODE


def test_nextweek_view_url_accessible_by_name(db, client):
    resp = client.get(reverse("issue:nextweek"))
    assert resp.status_code == HTML_OK_CODE


def test_nextweek_view_uses_correct_template(db, client):
    resp = client.get(reverse("issue:nextweek"))
    assert resp.status_code == HTML_OK_CODE
    assertTemplateUsed(resp, "comicsdb/week_list.html")


# Future week tests
def test_future_view_url_exists_at_desired_location(db, client):
    resp = client.get("/issue/future")
    assert resp.status_code == HTML_OK_CODE


def test_future_view_url_accessible_by_name(db, client):
    resp = client.get(reverse("issue:future"))
    assert resp.status_code == HTML_OK_CODE


def test_future_view_uses_correct_template(db, client):
    resp = client.get(reverse("issue:future"))
    assert resp.status_code == HTML_OK_CODE
    assertTemplateUsed(resp, "comicsdb/week_list.html")


# TODO: Add test for issues with a store date greater than next weeks.
