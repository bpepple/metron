import pytest

# from django.template.defaultfilters import slugify
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from comicsdb.models import Creator

HTML_OK_CODE = 200
HTML_REDIRECT_CODE = 302

PAGINATE_TEST_VAL = 35
PAGINATE_DEFAULT_VAL = 28
PAGINATE_DIFF_VAL = PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL


@pytest.fixture
def list_of_creators(create_user):
    user = create_user()
    for pub_num in range(PAGINATE_TEST_VAL):
        Creator.objects.create(
            name=f"John-Smith-{pub_num}",
            slug=f"john-smith-{pub_num}",
            edited_by=user,
        )


# Creator Views
def test_update_view_url_accessible_by_name(auto_login_user, john_byrne):
    client, _ = auto_login_user()
    resp = client.get(reverse("creator:update", kwargs={"slug": john_byrne.slug}))
    assert resp.status_code == HTML_OK_CODE


# def test_creator_update_view(auto_login_user, john_byrne):
#     client, user = auto_login_user()
#     new_name = "JB"
#     resp = client.post(
#         reverse("creator:update", kwargs={"slug": john_byrne.slug}),
#         {"name": new_name, "slug": john_byrne.slug, "edited_by": user},
#     )
#     assert resp.status_code == HTML_REDIRECT_CODE
#     john_byrne.refresh_from_db()
#     assert john_byrne.name == new_name


# def test_creator_create_view(auto_login_user):
#     client, user = auto_login_user()
#     name = "Jack Kirby"
#     resp = client.post(
#         reverse("creator:create"),
#         {"name": name, "slug": slugify(name), "edited_by": user},
#     )
#     assert resp.status_code == HTML_REDIRECT_CODE
#     c = Creator.objects.get(slug=slugify(name))
#     assert c is not None
#     assert c.name == name


# Creator Search
def test_creator_search_view_url_exists_at_desired_location(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get("/creator/search")
    assert resp.status_code == HTML_OK_CODE


def test_creator_search_view_url_accessible_by_name(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get(reverse("creator:search"))
    assert resp.status_code == HTML_OK_CODE


def test_creator_search_view_uses_correct_template(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get(reverse("creator:search"))
    assert resp.status_code == HTML_OK_CODE
    assertTemplateUsed(resp, "comicsdb/creator_list.html")


def test_creator_search_pagination_is_thirty(auto_login_user, list_of_creators):
    client, _ = auto_login_user()
    resp = client.get("/creator/search?q=smith")
    assert resp.status_code == HTML_OK_CODE
    assert "is_paginated" in resp.context
    assert resp.context["is_paginated"] is True
    assert len(resp.context["creator_list"]) == PAGINATE_DEFAULT_VAL


def test_creator_search_lists_all_creators(auto_login_user, list_of_creators):
    # Get second page and confirm it has (exactly) remaining 7 items
    client, _ = auto_login_user()
    resp = client.get("/creator/search?page=2&q=smith")
    assert resp.status_code == HTML_OK_CODE
    assert "is_paginated" in resp.context
    assert resp.context["is_paginated"] is True
    assert len(resp.context["creator_list"]) == PAGINATE_DIFF_VAL


# CreatorList
def test_creator_list_view_url_exists_at_desired_location(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get("/creator/")
    assert resp.status_code == HTML_OK_CODE


def test_creator_list_view_url_accessible_by_name(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get(reverse("creator:list"))
    assert resp.status_code == HTML_OK_CODE


def test_creator_list_view_uses_correct_template(auto_login_user):
    client, _ = auto_login_user()
    resp = client.get(reverse("creator:list"))
    assert resp.status_code == HTML_OK_CODE
    assertTemplateUsed(resp, "comicsdb/creator_list.html")


def test_creator_list_pagination_is_thirty(auto_login_user, list_of_creators):
    client, _ = auto_login_user()
    resp = client.get(reverse("creator:list"))
    assert resp.status_code == HTML_OK_CODE
    assert "is_paginated" in resp.context
    assert resp.context["is_paginated"] is True
    assert len(resp.context["creator_list"]) == PAGINATE_DEFAULT_VAL


def test_creator_list_lists_second_page(auto_login_user, list_of_creators):
    # Get second page and confirm it has (exactly) remaining 7 items
    client, _ = auto_login_user()
    resp = client.get(reverse("creator:list") + "?page=2")
    assert resp.status_code == HTML_OK_CODE
    assert "is_paginated" in resp.context
    assert resp.context["is_paginated"] is True
    assert len(resp.context["creator_list"]) == PAGINATE_DIFF_VAL
