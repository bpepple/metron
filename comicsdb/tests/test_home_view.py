from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

HTML_OK_CODE = 200


def test_view_url_exists_at_desired_location(db, client):
    resp = client.get("/")
    assert resp.status_code == HTML_OK_CODE


def test_view_url_accessible_by_name(db, client):
    resp = client.get(reverse("home"))
    assert resp.status_code == HTML_OK_CODE


def test_view_uses_correct_template(db, client):
    resp = client.get(reverse("home"))
    assert resp.status_code == HTML_OK_CODE
    assertTemplateUsed(resp, "comicsdb/home.html")
