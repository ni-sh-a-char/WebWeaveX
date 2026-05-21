CIVILIZATION_KEYS = frozenset(
    {
        "epistemic_openness",
        "semantic_plurality",
        "interpretive_diversity",
        "semantic_decentralization",
        "ontology_instability",
        "worldview_diversity",
        "explanatory_diversity",
    }
)


def assert_civilization_bundle(obj: dict) -> None:
    for key in CIVILIZATION_KEYS:
        assert key in obj, f"missing civilization key: {key}"
    assert obj["epistemic_openness"].get("anti_closure") is True
    assert obj["semantic_plurality"].get("preserved") is True
