from core.evidence import apply_recursive_reality_integrity


def test_performance():
    base = {
        "evidence": [],
        "ambiguities": [],
        "uncertainties": [],
        "observed": {},
        "inferred": {"x": 1},
        "reconciled": {"x": 1},
        "contradicted": {},
        "confidence_basis": {"score": 0.5},
        "fragility": {"level": "high", "confidence_limits": {"max_score": 0.4}},
        "lineage": {"stages": [{"stage": "a"}, {"stage": "b"}, {"stage": "c"}]},
        "instability": {"regions": []},
        "unstable_regions": [],
    }
    for _ in range(40):
        apply_recursive_reality_integrity(dict(base))
