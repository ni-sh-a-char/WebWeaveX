from core.evidence import apply_truth_preservation


def test_performance():
    base = {
        "evidence": [],
        "ambiguities": ["a"],
        "uncertainties": [],
        "observed": {},
        "inferred": {"x": 1},
        "reconciled": {"x": 1},
        "contradicted": {},
        "confidence_basis": {"score": 0.5},
        "fragility": {"level": "high", "confidence_limits": {"max_score": 0.4}},
        "unstable_regions": [],
    }
    for _ in range(40):
        apply_truth_preservation(dict(base))
