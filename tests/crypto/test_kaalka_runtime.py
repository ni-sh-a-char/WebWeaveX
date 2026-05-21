import json
from pathlib import Path

from core.crypto.kaalka_runtime_engine import (
    decrypt_value,
    encrypt_value,
    normalize_runtime_value,
)


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "kaalka_cross_language.json"


def test_deterministic_encryption():
    first = encrypt_value("hello", "key")
    second = encrypt_value("hello", "key")

    assert first["encrypted"] == second["encrypted"]
    assert first["deterministic"] is True
    assert first["algorithm"] == "kaalka"


def test_round_trip():
    original = "WebWeaveX runtime"
    encrypted = encrypt_value(original, "secret-key")
    decrypted = decrypt_value(encrypted["encrypted"], "secret-key")

    assert decrypted["decrypted"] == original


def test_cross_language_stability_fixture():
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    result = encrypt_value(fixture["value"], fixture["key"])

    assert result["encrypted"] == fixture["expected"]


def test_normalization_newlines():
    assert normalize_runtime_value("a\r\nb\r c") == "a\nb\n c"
