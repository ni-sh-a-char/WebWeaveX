OPENNESS_KEYS = frozenset(
    {
        "civilizational_openness",
        "semantic_divergence",
        "recursive_novelty",
        "worldview_variance",
        "interpretive_divergence",
        "ontology_divergence",
        "explanatory_divergence",
    }
)


def assert_openness_bundle(obj: dict) -> None:
    for key in OPENNESS_KEYS:
        assert key in obj, f"missing openness key: {key}"
    assert obj["civilizational_openness"].get("open") is True
    assert obj["civilizational_openness"].get("anti_convergence") is True
    assert obj["exploratory_capacity"].get("collapse_blocked") is True
