from core.evidence import apply_recursive_epistemic_sovereignty


def test_performance():
    base = {
        "evidence": ["e1", "e2"],
        "observed": {"a": 1},
        "inferred": {"b": 2},
        "reconciled": {"a": 1},
        "interpretive_diversity": {"interpretations": [{"id": "a"}, {"id": "b"}]},
        "explanatory_diversity": {"alternatives": [{"x": 1}]},
        "lineage": {"stages": [{"s": 1}, {"s": 2}]},
        "confidence_basis": {"score": 0.5},
        "cognitive_decentralization": {"dominance_without_evidence": False},
    }
    for _ in range(40):
        apply_recursive_epistemic_sovereignty(dict(base))
