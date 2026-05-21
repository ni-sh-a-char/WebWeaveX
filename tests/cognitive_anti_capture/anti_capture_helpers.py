ANTI_CAPTURE_KEYS = frozenset(
    {
        "cognitive_anti_capture",
        "semantic_autonomy",
        "interpretive_autonomy",
        "ontology_competition",
        "explanatory_competition",
        "semantic_freedom",
        "cognitive_decentralization",
    }
)


def assert_anti_capture_bundle(obj: dict) -> None:
    for key in ANTI_CAPTURE_KEYS:
        assert key in obj, f"missing anti-capture key: {key}"
    assert obj["cognitive_anti_capture"].get("active") is True
    assert obj["capture_resistance"].get("resistant") is True
