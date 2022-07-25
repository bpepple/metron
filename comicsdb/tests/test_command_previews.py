from comicsdb.management.commands.import_previews import Command


def test_check_valid_publisher() -> None:
    cmd = Command()
    result = cmd._check_valid_publisher("IMAGE COMICS")
    assert result is True


def test_check_invalid_publisher() -> None:
    cmd = Command()
    result = cmd._check_valid_publisher("DC COMICS")
    assert result is False


def test_valid_decimal() -> None:
    cmd = Command()
    result = cmd._is_decimal("1.2")
    assert result is True


def test_invalid_decimal() -> None:
    cmd = Command()
    result = cmd._is_decimal("A")
    assert result is False


def test_preview_data(preview_data: str) -> None:
    cmd = Command()
    result = cmd._remove_intro_text(preview_data)
    assert len(result) == 24
    result = cmd._remove_empty_items(result)
    assert len(result) == 23
