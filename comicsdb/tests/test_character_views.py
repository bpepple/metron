from comicsdb.forms.character import CharacterForm
from comicsdb.models import Character
from django.urls import reverse
from users.tests.case_base import TestCaseBase

HTML_OK_CODE = 200

PAGINATE_TEST_VAL = 35
PAGINATE_DEFAULT_VAL = 28
PAGINATE_DIFF_VAL = PAGINATE_TEST_VAL - PAGINATE_DEFAULT_VAL


class CharacterSearchViewsTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        for pub_num in range(PAGINATE_TEST_VAL):
            Character.objects.create(
                name="Character %s" % pub_num,
                slug="character-%s" % pub_num,
                edited_by=user,
            )

    def setUp(self):
        self._client_login()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get("/character/search")
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("character:search"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse("character:search"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, "comicsdb/character_list.html")

    def test_pagination_is_thirty(self):
        resp = self.client.get("/character/search?q=char")
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["character_list"]) == PAGINATE_DEFAULT_VAL)

    def test_lists_all_characters(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get("/character/search?page=2&q=char")
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["character_list"]) == PAGINATE_DIFF_VAL)


class CharacterListViewTest(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        for pub_num in range(PAGINATE_TEST_VAL):
            Character.objects.create(
                name="Character %s" % pub_num,
                slug="character-%s" % pub_num,
                edited_by=user,
            )

    def setUp(self):
        self._client_login()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get("/character/")
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("character:list"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse("character:list"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(resp, "comicsdb/character_list.html")

    def test_pagination_is_thirty(self):
        resp = self.client.get(reverse("character:list"))
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["character_list"]) == PAGINATE_DEFAULT_VAL)

    def test_lists_second_page(self):
        # Get second page and confirm it has (exactly) remaining 7 items
        resp = self.client.get(reverse("character:list") + "?page=2")
        self.assertEqual(resp.status_code, HTML_OK_CODE)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"])
        self.assertTrue(len(resp.context["character_list"]) == PAGINATE_DIFF_VAL)


class TestCharacterForm(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        cls._create_user()

    def setUp(self):
        self._client_login()

    def test_valid_form(self):
        form = CharacterForm(
            data={
                "name": "Batman",
                "slug": "batman",
                "desc": "The Dark Knight.",
                "wikipedia": "Batman",
                "image": "character/2019/06/07/batman.jpg",
                "alias": "Dark Knight",
                "creators": "",
                "teams": "",
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = CharacterForm(
            data={
                "name": "",
                "slug": "bad-data",
                "desc": "",
                "wikipedia": "",
                "image": "",
                "alias": "",
                "creators": "",
                "teams": "",
            }
        )
        self.assertFalse(form.is_valid())


class TestCharacterCreate(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        cls._create_user()

    def setUp(self):
        self._client_login()

    def test_create_character_view(self):
        response = self.client.get(reverse("character:create"))
        self.assertEqual(response.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(response, "comicsdb/model_with_image_form.html")

    def test_create_character_validform_view(self):
        character_count = Character.objects.count()
        response = self.client.post(
            reverse("character:create"),
            {
                "name": "Hulk",
                "slug": "hulk",
                "desc": "Gamma powered goliath.",
                "wikipedia": "Hulk",
                "image": "character/2019/06/07/hulk.jpg",
                "alias": "Green Goliath",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Character.objects.count(), character_count + 1)


class TestCharacterUpdate(TestCaseBase):
    @classmethod
    def setUpTestData(cls):
        user = cls._create_user()

        cls.slug = "hulk"
        Character.objects.create(
            name="Hulk",
            slug=cls.slug,
            desc="Gamma powered goliath.",
            wikipedia="Hulk",
            image="character/2019/06/07/hulk.jpg",
            edited_by=user,
        )

    def setUp(self):
        self._client_login()

    def test_character_update_view(self):
        k = {"slug": self.slug}
        response = self.client.get(reverse("character:update", kwargs=k))
        self.assertEqual(response.status_code, HTML_OK_CODE)
        self.assertTemplateUsed(response, "comicsdb/model_with_image_form.html")

    def test_character_update_validform_view(self):
        k = {"slug": self.slug}
        character_count = Character.objects.count()
        response = self.client.post(
            reverse("character:update", kwargs=k),
            {
                "name": "Hulk",
                "slug": self.slug,
                "desc": "Big Green Fighting Machine.",
                "wikipedia": "Hulk",
                "image": "character/2019/06/07/hulk.jpg",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Character.objects.count(), character_count)
