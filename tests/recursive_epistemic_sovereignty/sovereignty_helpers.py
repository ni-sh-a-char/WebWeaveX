SOVEREIGNTY_KEYS = frozenset(
    {
        "epistemic_sovereignty",
        "semantic_self_determination",
        "interpretive_self_determination",
        "ontology_self_determination",
        "explanatory_self_determination",
        "recursive_agency",
        "cognitive_sovereignty",
    }
)


def assert_sovereignty_bundle(obj: dict) -> None:
    for key in SOVEREIGNTY_KEYS:
        assert key in obj, f"missing sovereignty key: {key}"
    assert obj["epistemic_sovereignty"].get("anti_dependent") is True
    assert obj["cognitive_sovereignty"].get("downstream_agency_required") is True
