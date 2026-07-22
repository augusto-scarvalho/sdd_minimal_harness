import pytest

from src.hello_transform import normalize_text


def test_normaliza_texto_valido():
    assert normalize_text("abc") == "abc"


def test_remove_espacos_extras():
    assert normalize_text("  abc  ") == "abc"


def test_rejeita_nulo():
    with pytest.raises(ValueError):
        normalize_text(None)


def test_rejeita_vazio():
    with pytest.raises(ValueError):
        normalize_text("   ")
