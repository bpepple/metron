import pytest
from django.contrib.auth.models import Group
from django.test import Client

from users.models import CustomUser


@pytest.fixture
def editor(db):
    grp = Group(user="editor")
    grp.save()
    user = CustomUser.objects.create(username="brian", email="brian@test.com")
    user.set_password("1234")
    user.groups.add(grp)
    user.save()
    return user


@pytest.fixture
def user(db):
    user = CustomUser.objects.create(username="foo", email="foo@bar.com")
    user.set_password("1234")
    user.save()
    return user


@pytest.fixture
def loggedin_user(db, user):
    client = Client()
    client.login(username="foo", password="1234")
    return client
