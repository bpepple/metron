import logging

from comicsdb.forms.arc import ArcForm
from comicsdb.models import Arc
from django.urls import reverse
from users.tests.case_base import TestCaseBase

HTML_OK_CODE = 200

PAGINATE_TEST_VAL = 35
PAGINATE_DEFAULT_VAL = 28
PAGINATE_DIFF_VAL = PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL


class ArcSearchViewsTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        for pub_num in range(PAGINATE_TEST_VAL):
            Arc.objects.create(
                name="Arc %s" % pub_num, slug="arc-%s" % pub_num, edited_by=user
            )

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self._client_login()

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get("/arc/search")
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("arc:search"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse("arc:search"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, "comicsdb/arc_list.html")

    def test_pagination_is_thirty(self):
        resp = self.client.get("/arc/search?q=arc")
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["arc_list"]) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_arcs(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get("/arc/search?page=2&q=arc")
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["arc_list"]) == PAGINATE_DIFF_VAL)


class ArcListViewTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        for pub_num in range(PAGINATE_TEST_VAL):
            Arc.objects.create(
                name="Arc %s" % pub_num, slug="arc-%s" % pub_num, edited_by=user
            )

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self._client_login()

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get("/arc/")
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("arc:list"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse("arc:list"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, "comicsdb/arc_list.html")

    def test_pagination_is_thirty(self):
        resp = self.client.get(reverse("arc:list"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["arc_list"]) == PAGINATE_DEFAULT_VAL)

    def test_lists_second_page(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get(reverse("arc:list") + "?page=2")
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["arc_list"]) == PAGINATE_DIFF_VAL)


class TestArcForm(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        cls._create_user()

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self._client_login()

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_valid_form(self):
        form = ArcForm(
            data={
                "name": "Heroes in Crisis",
                "slug": "heroes-in-crisis",
                "desc": "Heroes in need of therapy",
                "image": "arc/2019/06/07/heroes-1.jpg",
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = ArcForm(data={"name": "", "slug": "bad-data", "desc": "", "image": ""})
        self.assertFalse(form.is_valid())


class TestArcCreate(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        cls._create_user()

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self._client_login()

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_create_arc_view(self):
        response = self.client.get(reverse("arc:create"))
        self.assertEqual(response.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(response, "comicsdb/model_with_image_form.html")

    def test_create_arc_validform_view(self):
        arc_count = Arc.objects.count()
        response = self.client.post(
            reverse("arc:create"),
            {
                "name": "Infinite Crisis",
                "slug": "infinite-crisis",
                "desc": "World ending crisis",
                "image": "arc/2019/06/07/crisis-1",
            },
        )
        # Should this really be HTTP 302? Probably need to see if we should be redirecting or not.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Arc.objects.count(), arc_count + 1)


class TestArcUpdate(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        cls.slug = "war-realms"
        cls.realms = Arc.objects.create(
            name="War of the Realms", slug=cls.slug, edited_by=user
        )

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self._client_login()

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_arc_update_view(self):
        k = {"slug": self.slug}
        response = self.client.get(reverse("arc:update", kwargs=k))
        self.assertEqual(response.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(response, "comicsdb/model_with_image_form.html")

    def test_arc_update_validform_view(self):
        k = {"slug": self.slug}
        arc_count = Arc.objects.count()
        response = self.client.post(
            reverse("arc:update", kwargs=k),
            {
                "name": "War of the Realms",
                "slug": self.slug,
                "desc": "Asgardian crisis",
                "image": "",
            },
        )
        # Should this really be HTTP 302? Probably need to see if we should be redirecting or not.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Arc.objects.count(), arc_count)
