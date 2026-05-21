from core.crdt.semantic_crdt_engine import (
    merge_semantic_states,
)


def test_crdt_merge():

    r = merge_semantic_states(
        {"x": 1},
        {"x": 2},
    )

    assert "state" in r
