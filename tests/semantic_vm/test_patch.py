from core.memory.semantic_patch_engine import (
    build_semantic_patch,
)


def test_patch():

    r = build_semantic_patch(
        {"a": 1},
        {"b": 2},
    )

    assert "b" in r["added"]
