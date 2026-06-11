"""One-shot generator: append the Phase D fixture set to fixtures.json."""
import json
import os

D = os.path.dirname(os.path.abspath(__file__))

DOC = "# Alpha\nintro line\n\n## Beta\nbody because reasons\n\n## Gamma\nend\n"

ALIGN_FULL = {
    "evidence": ["e1"],
    "ambiguities": ["amb1"],
    "uncertainties": {"u1": 1},
    "observed": {"o1": 1},
    "inferred": {"i1": 1, "i2": 2},
    "reconciled": {"i1": 1, "i2": 2},
    "contradicted": {"pairs": [["x", "y"]]},
    "confidence_basis": {"score": 0.85},
    "parser_basis": {"symbol_count": 2},
    "noninferable_regions": ["zone1"],
    "fragility": {"level": "high", "confidence_limits": {"max_score": 0.6}},
    "termination_reasons": ["seed_reason"],
    "semantic_limits": {"existing": True},
}

ALIGN_UNGROUNDED = {
    "evidence": [],
    "inferred": {"a": 1},
    "reconciled": {},
    "uncertain": ["u-list"],
    "fragility": "notadict",
    "confidence_basis": {"score": 0.4},
}

B = []


def fx(i, fn, args, kwargs=None):
    f = {"id": i, "fn": fn, "args": args}
    if kwargs:
        f["kwargs"] = kwargs
    B.append(f)


fx("d-transitions-doc", "model_concept_transitions", [DOC])
fx("d-transitions-empty", "model_concept_transitions", [""])
fx("d-spec-gap", "detect_semantic_speculation",
   [["e1"], {"i1": 1, "i2": 2}, {"r": 1}])
fx("d-spec-ok", "detect_semantic_speculation", [["e1", "e2"], {}, {}])
fx("d-collapse-plain", "apply_confidence_collapse", [0.8, {}])
fx("d-collapse-full", "apply_confidence_collapse",
   [0.9, {"confidence_limits": {"max": 0.7}}],
   {"reinforcement_count": 2, "stabilization_count": 1, "decay_pressure": 0.4,
    "truth_boundary_pressure": 0.3, "contradiction_count": 1,
    "ambiguity_count": 1, "uncertainty_count": 2, "incompleteness": True})
fx("d-collapse-partial", "apply_confidence_collapse", [0.5, {}],
   {"reinforcement_count": 3, "incompleteness": True})
fx("d-align-full", "apply_reality_alignment", [ALIGN_FULL])
fx("d-align-ungrounded", "apply_reality_alignment", [ALIGN_UNGROUNDED])
fx("d-align-empty", "apply_reality_alignment", [{}])
fx("d-align-grounding", "apply_reality_alignment",
   [{"evidence": ["e1", "e2"], "observed": {"o": 1}, "inferred": {"o": 1},
     "reconciled": {"o": 1}, "grounding": {"language": "python"},
     "confidence_basis": {"score": 0.65}}])

path = os.path.join(D, "fixtures.json")
existing = json.load(open(path, encoding="utf-8-sig"))
ids = {f["id"] for f in existing}
assert not ids & {f["id"] for f in B}
merged = existing + B
with open(path, "w", encoding="utf-8") as fh:
    json.dump(merged, fh, ensure_ascii=False, indent=1)
print(f"added {len(B)} Phase D fixtures -> {len(merged)} total")
