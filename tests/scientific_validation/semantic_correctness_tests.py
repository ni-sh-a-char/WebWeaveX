from core.evidence import build_semantic_integrity_object
from tests.scientific_validation.scientific_helpers import assert_measurable
from benchmarks.evaluators import eval_semantic_consistency


def test_semantic_consistency_evaluator():
    case = {
        "input": {"observed": {"a": 1}, "inferred": {}, "reconciled": {"a": 1}},
        "expected": {"consistent": True},
    }
    r = eval_semantic_consistency(case)
    assert r["predicted"] is True


def test_bundle_has_proof():
    b = build_semantic_integrity_object(observed={"x": 1}, inferred={}, reconciled={"x": 1})
    assert b["semantic_proof"]["proved"] is True
    assert b["justification"]["opaque"] is False
