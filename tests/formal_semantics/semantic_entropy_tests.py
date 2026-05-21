from core.evidence import build_semantic_integrity_object
from tests.formal_semantics.formal_helpers import assert_formal_bundle


def test_entropy_on_bundle():
    r = build_semantic_integrity_object(
        observed={"a": 1},
        inferred={"b": 2},
        ambiguities=["x"],
        contradicted={"pairs": [["a", "b"]]},
    )
    assert_formal_bundle(r)
    assert r["entropy"]["entropy"] > 0
