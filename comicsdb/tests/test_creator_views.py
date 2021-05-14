from comicsdb.models import Creator
from django.template.defaultfilters import slugify
from django.urls import reverse
from users.tests.case_base import TestCaseBase

HTML_OK_CODE = 200
HTML_REDIRECT_CODE = 302

PAGINATE_TEST_VAL = 35
PAGINATE_DEFAULT_VAL = 28
PAGINATE_DIFF_VAL = PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL


class CreatorViewsTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls._create_user()
        name = "John Smith"
        cls.slug = slugify(name)
        cls.creator = Creator.objects.create(
            name=name, slug=cls.slug, edited_by=cls.user
        )

    def setUp(self):
        self._client_login()

    def test_update_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("creator:update", kwargs={"slug": self.slug}))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_creator_update_view(self):
        name = "John Byrne"
        resp = self.client.post(
            reverse("creator:update", kwargs={"slug": self.slug}),
            {"name": name, "slug": slugify(name), "edited_by": self.user},
        )
        self.assertEqual(resp.status_code, HTML_REDIRECT_CODE)
        self.creator.refresh_from_db()
        self.assertEqual(self.creator.name, name)

    def test_creator_create_view(self):
        name = "Walter Simonson"
        resp = self.client.post(
            reverse("creator:create"),
            {"name": name, "slug": slugify(name), "edited_by": self.user},
        )
        self.assertEqual(resp.status_code, HTML_REDIRECT_CODE)
        c = Creator.objects.get(slug=slugify(name))
        self.assertIsNotNone(c)
        self.assertEqual(c.name, name)


class CreatorSearchViewsTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        for pub_num in range(PAGINATE_TEST_VAL):
            Creator.objects.create(
                name=f"John-Smith-{pub_num}",
                slug=f"john-smith-{pub_num}",
                edited_by=user,
            )

    def setUp(self):
        self._client_login()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get("/creator/search")
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("creator:search"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse("creator:search"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, "comicsdb/creator_list.html")

    def test_pagination_is_thirty(self):
        resp = self.client.get("/creator/search?q=smith")
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["creator_list"]) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_creators(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get("/creator/search?page=2&q=smith")
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["creator_list"]) == PAGINATE_DIFF_VAL)


class CreatorListViewTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        for pub_num in range(PAGINATE_TEST_VAL):
            Creator.objects.create(
                name=f"John-Smith-{pub_num}",
                slug=f"john-smith-{pub_num}",
                edited_by=user,
            )

    def setUp(self):
        self._client_login()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get("/creator/")
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("creator:list"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse("creator:list"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, "comicsdb/creator_list.html")

    def test_pagination_is_thirty(self):
        resp = self.client.get(reverse("creator:list"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["creator_list"]) == PAGINATE_DEFAULT_VAL)

    def test_lists_second_page(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get(reverse("creator:list") + "?page=2")
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["creator_list"]) == PAGINATE_DIFF_VAL)
