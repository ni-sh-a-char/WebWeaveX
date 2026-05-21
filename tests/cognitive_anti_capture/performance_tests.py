from core.evidence import apply_cognitive_anti_capture


def test_performance():
    base = {
        "evidence": ["e1", "e2"],
        "ambiguities": [],
        "observed": {"a": 1},
        "inferred": {"b": 2},
        "reconciled": {"a": 1},
        "contradicted": {},
        "interpretive_diversity": {"interpretations": [{"id": "a"}, {"id": "b"}]},
        "explanatory_diversity": {"alternatives": [{"x": 1}, {"y": 2}]},
        "lineage": {"stages": [{"s": 1}]},
        "confidence_basis": {"score": 0.5},
        "unstable_regions": [],
    }
    for _ in range(40):
        apply_cognitive_anti_capture(dict(base))
