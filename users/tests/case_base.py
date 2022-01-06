from django.contrib.auth.models import Group, Permission
from django.test import TestCase

from users.models import CustomUser


class TestCaseBase(TestCase):
    @classmethod
    def _create_user(cls):
        user = CustomUser.objects.create(username="brian", email="brian@test.com")
        user.set_password("1234")
        user.save()

        # TODO: Need to split the group bit out for better test coverage (post, delete, etc)
        contributor_group = Group.objects.create(name="contributor")
        permission_codename = ["view_arc"]
        for permission in permission_codename:
            perm = Permission.objects.filter(codename=permission).first()
            contributor_group.permissions.add(perm)
        user.groups.add(contributor_group)

        return user

    def _client_login(self):
        self.client.login(username="brian", password="1234")
