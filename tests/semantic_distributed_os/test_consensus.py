from core.consensus.semantic_consensus_engine import (
    compute_semantic_consensus,
)


def test_consensus():

    r = compute_semantic_consensus([
        {"value": "a"},
        {"value": "a"},
    ])

    assert r["consensus"] == "a"
