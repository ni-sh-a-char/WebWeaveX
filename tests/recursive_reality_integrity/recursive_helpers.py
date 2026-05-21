RECURSIVE_KEYS = frozenset(
    {
        "recursive_reality_integrity",
        "recursive_entropy",
        "recursive_instability",
        "recursive_truth_boundaries",
        "recursive_drift",
        "recursive_semantic_closure",
        "recursive_confidence_decay",
        "recursive_uncertainty",
    }
)


def assert_recursive_bundle(obj: dict) -> None:
    for key in RECURSIVE_KEYS:
        assert key in obj, f"missing recursive key: {key}"
    assert obj["recursive_entropy"].get("preserved") is True
    assert obj["recursive_reality_integrity"].get("preserved") is True
