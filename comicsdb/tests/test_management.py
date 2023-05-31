import pytest
from django.core.management import call_command

from comicsdb.models.arc import Arc
from comicsdb.models.character import Character
from users.models import CustomUser

FAKE_CVID = 9999
FAKE_DESC = "Duplicate Object"
FAKE_ALIAS = ["Clark Kent"]


@pytest.fixture()
def other_character(create_user: CustomUser) -> Character:
    user = create_user()
    return Character.objects.create(
        name="Superman",
        desc=FAKE_DESC,
        cv_id=FAKE_CVID,
        alias=FAKE_ALIAS,
        edited_by=user,
    )


def test_merge_characters(superman: Character, other_character: Character) -> None:
    call_command("merge_characters", canonical=superman.id, other=other_character.id)
    superman.refresh_from_db()
    assert superman.cv_id == FAKE_CVID
    assert superman.desc == FAKE_DESC
    assert superman.alias == FAKE_ALIAS


@pytest.fixture
def other_arc(create_user: CustomUser) -> Arc:
    user = create_user()
    return Arc.objects.create(
        name="Final Crisis", desc=FAKE_DESC, cv_id=FAKE_CVID, edited_by=user
    )


def test_merge_arcs(fc_arc: Arc, other_arc: Arc) -> None:
    call_command("merge_arcs", canonical=fc_arc.id, other=other_arc.id)
    fc_arc.refresh_from_db()
    assert fc_arc.cv_id == FAKE_CVID
    assert fc_arc.desc == FAKE_DESC
