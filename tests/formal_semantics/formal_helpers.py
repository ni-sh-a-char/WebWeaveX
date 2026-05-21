FORMAL_KEYS = frozenset(
    {
        "observed",
        "inferred",
        "reconciled",
        "evidence",
        "lineage",
        "uncertainty",
        "entropy",
        "contradictions",
        "confidence_basis",
        "justification",
        "deterministic_inputs",
    }
)


def assert_formal_bundle(obj: dict) -> None:
    for key in FORMAL_KEYS:
        assert key in obj, f"missing formal key: {key}"
    assert obj["justification"].get("opaque") is False
    assert obj["justification"].get("explainable") is True
    assert isinstance(obj["deterministic_inputs"], list)
