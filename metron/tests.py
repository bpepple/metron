import pytest
from django.test import Client

from users.models import CustomUser

HTML_OK_CODE = 200


@pytest.fixture
def loggedin_user(db):
    user = CustomUser.objects.create(username="foo", email="foo@bar.com")
    user.set_password("1234")
    user.save()

    client = Client()
    client.login(username="foo", password="1234")
    return client


def test_api_docs_url_exists_at_desired_location(loggedin_user):
    resp = loggedin_user.get("/docs/")
    assert resp.status_code == HTML_OK_CODE
