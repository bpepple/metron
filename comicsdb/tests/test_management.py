from django.core.management import call_command

from comicsdb.models.character import Character


def test_merge_characters(superman: Character):
    cv_id = 9999
    desc = "Duplicate entry"
    alias = ["Clark Kent"]
    test_character = Character.objects.create(
        name="Superman", desc=desc, cv_id=cv_id, alias=alias
    )
    call_command("merge_characters", canonical=superman.id, other=test_character.id)
    superman.refresh_from_db()
    assert superman.cv_id == cv_id
    assert superman.desc == desc
    assert superman.alias == alias
