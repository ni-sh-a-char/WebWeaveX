from core.evidence import build_semantic_integrity_object
from tests.formal_semantics.formal_helpers import assert_formal_bundle


def test_full_formal_grounding():
    r = build_semantic_integrity_object(observed={"x": 1}, inferred={}, reconciled={"x": 1})
    assert_formal_bundle(r)
    assert len(r["deterministic_inputs"]) > 0
