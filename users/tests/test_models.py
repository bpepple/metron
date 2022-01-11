from users.models import CustomUser


def test_user_creation(editor):
    assert isinstance(editor, CustomUser) is True
    assert str(editor) == editor.username
