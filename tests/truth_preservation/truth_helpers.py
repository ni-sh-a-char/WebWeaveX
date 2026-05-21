TRUTH_KEYS = frozenset(
    {
        "truth_preservation",
        "semantic_decay",
        "confidence_collapse",
        "instability",
        "truth_boundaries",
        "unsupported_stabilization",
        "semantic_entropy",
        "evidence_decay",
    }
)


def assert_truth_bundle(obj: dict) -> None:
    for key in TRUTH_KEYS:
        assert key in obj, f"missing truth key: {key}"
    assert obj["truth_preservation"].get("prefer_truthfully_incomplete") is True
    assert obj["semantic_entropy"].get("preserved") is True
