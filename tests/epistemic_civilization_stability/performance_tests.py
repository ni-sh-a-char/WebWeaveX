from core.evidence import apply_epistemic_civilization_stability


def test_performance():
    base = {
        "evidence": ["e1"],
        "ambiguities": [],
        "observed": {"a": 1},
        "inferred": {"b": 2},
        "reconciled": {"a": 1},
        "contradicted": {},
        "lineage": {"stages": [{"s": 1}]},
        "unstable_regions": [],
    }
    for _ in range(40):
        apply_epistemic_civilization_stability(dict(base))
