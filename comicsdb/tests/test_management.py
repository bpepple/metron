from django.core.management import call_command

from comicsdb.models.arc import Arc
from comicsdb.models.character import Character


def test_merge_characters(superman: Character):
    cv_id = 9999
    desc = "Duplicate entry"
    alias = ["Clark Kent"]
    other_obj = Character.objects.create(name="Superman", desc=desc, cv_id=cv_id, alias=alias)
    call_command("merge_characters", canonical=superman.id, other=other_obj.id)
    superman.refresh_from_db()
    assert superman.cv_id == cv_id
    assert superman.desc == desc
    assert superman.alias == alias


def test_merge_arcs(fc_arc: Arc):
    cv_id = 1000
    desc = "Dup Arc"
    other_obj = Arc.objects.create(name="Final Crisis", desc=desc, cv_id=cv_id)
    call_command("merge_arcs", canonical=fc_arc.id, other=other_obj.id)
    fc_arc.refresh_from_db()
    assert fc_arc.cv_id == cv_id
    assert fc_arc.desc == desc
