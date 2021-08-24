import logging

from django.urls import reverse

from comicsdb.models import Publisher
from users.tests.case_base import TestCaseBase


class PublisherUpdateTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()
        cls.dc = Publisher.objects.create(name="DC Comics", slug="dc-comics", edited_by=user)

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self._client_login()

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_publisher_update(self):
        resp = self.client.post(
            reverse("publisher:update", kwargs={"slug": self.dc.slug}),
            {"name": "DC Comics", "slug": "dc-comics", "desc": "Test data"},
        )
        self.assertEqual(resp.status_code, 302)
        self.dc.refresh_from_db()
        self.assertEqual(self.dc.desc, "Test data")
