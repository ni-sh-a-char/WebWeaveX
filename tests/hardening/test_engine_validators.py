"""Invoke built-in validate_* self-checks on extraction engine."""

from core.extraction_engine import validate_extraction_engine


def test_extraction_engine_validator():
    assert validate_extraction_engine() is True
