import pytest

from src.hello_transform import normalize_text


def test_normalizes_valid_text():
    assert normalize_text("abc") == "abc"


def test_strips_surrounding_spaces():
    assert normalize_text("  abc  ") == "abc"


def test_rejects_none():
    with pytest.raises(ValueError):
        normalize_text(None)


def test_rejects_empty():
    with pytest.raises(ValueError):
        normalize_text("   ")
