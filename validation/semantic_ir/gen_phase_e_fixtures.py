"""One-shot generator: append the Phase E fixture set to fixtures.json."""
import json
import os

D = os.path.dirname(os.path.abspath(__file__))

DOC = ("# Setup guide\nintro because reasons\n\n## Step one: install\nbody\n\n"
       "## Step two: verify\nTherefore done.\n")

HUM_FULL = {
    "evidence": ["e1"],
    "ambiguities": ["amb1", "amb2"],
    "uncertainties": {"u1": 1},
    "inferred": {"i1": 1, "i2": 2},
    "reconciled": {"i1": 1},
    "noninference_reasons": ["nr1"],
    "contradicted": {"pairs": [["x", "y"]]},
    "parser_basis": {"symbol_count": 0},
    "confidence_basis": {"score": 0.9},
    "unsupported_expansions": ["ux1"],
    "refused_inferences": ["ri1"],
    "fragility": "notadict",
    "boundaries": {"existing": True},
}

TRUTH_FULL = {
    "evidence": ["e1"],
    "ambiguities": ["amb1"],
    "uncertain": ["u-list"],
    "inferred": {"a": 1},
    "reconciled": {"a": 1},
    "contradictions": {"pairs": [["p", "q"]]},
    "unstable_regions": ["zone1"],
    "semantic_fragility": {"level": "high",
                           "confidence_limits": {"max_score": 0.6}},
    "confidence_basis": {"score": 0.97},
    "termination_reasons": ["seed"],
    "semantic_limits": {"existing": True},
}

B = []


def fx(i, fn, args, kwargs=None):
    f = {"id": i, "fn": fn, "args": args}
    if kwargs:
        f["kwargs"] = kwargs
    B.append(f)


fx("e-docgraph-doc", "build_document_dependency_graph", [DOC])
fx("e-docgraph-empty", "build_document_dependency_graph", [""])
fx("e-semtrans-doc", "model_semantic_transitions", [DOC])
fx("e-semtrans-empty", "model_semantic_transitions", [""])
fx("e-recdecay-plain", "apply_recursive_confidence_decay", [0.8, {}])
fx("e-recdecay-full", "apply_recursive_confidence_decay",
   [0.95, {"confidence_limits": {"max": 0.8}}],
   {"depth": 3, "closure_count": 2, "drift_pressure": 0.3, "entropy": 0.5,
    "contradiction_count": 1, "ambiguity_count": 1, "uncertainty_count": 1})
fx("e-recdecay-partial", "apply_recursive_confidence_decay", [0.6, {}],
   {"depth": 5, "entropy": 0.9})
fx("e-humility-full", "apply_cognitive_humility", [HUM_FULL])
fx("e-humility-empty", "apply_cognitive_humility", [{}])
fx("e-humility-grounded", "apply_cognitive_humility",
   [{"evidence": ["e1", "e2", "e3"], "inferred": {"i": 1},
     "parser_basis": {"symbol_count": 4},
     "confidence_basis": {"score": 0.55}}])
fx("e-truth-full", "apply_truth_preservation", [TRUTH_FULL])
fx("e-truth-empty", "apply_truth_preservation", [{}])
fx("e-truth-echo", "apply_truth_preservation",
   [{"evidence": ["e1", "e2"], "inferred": {"a": 1}, "reconciled": {"b": 2},
     "confidence_basis": {"score": 0.99}}])

path = os.path.join(D, "fixtures.json")
existing = json.load(open(path, encoding="utf-8-sig"))
ids = {f["id"] for f in existing}
assert not ids & {f["id"] for f in B}
merged = existing + B
with open(path, "w", encoding="utf-8") as fh:
    json.dump(merged, fh, ensure_ascii=False, indent=1)
print(f"added {len(B)} Phase E fixtures -> {len(merged)} total")
