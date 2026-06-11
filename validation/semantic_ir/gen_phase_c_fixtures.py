"""One-shot generator: append the Phase C fixture set to fixtures.json."""
import json
import os

D = os.path.dirname(os.path.abspath(__file__))

PY_SRC = (
    "import os\nfrom typing import Any\n\ndef handler(event, context=None):\n"
    "    payload = event\n    return payload\n\nclass Service:\n"
    "    def run(self):\n        state = 1\n        return state\n\nlimit = 10\n"
)

COREF_TEXT = (
    "# Engine\nThe engine parses documents. It is deterministic.\n\n"
    "# Pipeline\nThis builds on the engine because of shared state.\n"
)

INSTR_TEXT = (
    "# Overview\nNote: read carefully.\n\n## Step one: install\n"
    "Warning: requires network.\n\n## Step two: setup\nDone.\n"
)

B_FULL = {
    "evidence": ["e1"],
    "ambiguities": ["amb1"],
    "observed": {"o1": 1, "o2": 2},
    "inferred": {"i1": 1, "i2": 2, "i3": 3, "i4": 4},
    "reconciled": {},
    "contradicted": {"pairs": [["x", "y"]], "preserved": True},
    "parser_basis": {"symbol_count": 3, "flags": {"ast": True}},
    "confidence_basis": {"score": 0.9, "supporting_evidence": ["s1"]},
    "epistemic_state": {"incomplete": True},
    "uncertainties": {"u1": 1, "u2": 2},
    "lineage": {"stages": [{"stage": "a"}, {"stage": "b"}, {"stage": "c"}]},
}

B_DIVERSE = {
    "evidence": ["e1", "e2", "e3"],
    "ambiguities": ["amb1", "amb2"],
    "observed": {"o1": 1},
    "inferred": {"i1": 1},
    "reconciled": {"r": 9},
    "interpretive_diversity": {"interpretations": [{"k": 1}, {"k": 2}]},
    "explanatory_diversity": {"alternatives": ["alt1", "alt2"]},
    "confidence_basis": {"score": 0.45},
    "uncertain": ["u-listy"],
    "unstable_regions": ["zone1"],
    "lineage": {"depth": 2, "stages": "notalist"},
}

B_SOVEREIGN = {
    "evidence": ["e1"],
    "inferred": {"a": 1},
    "reconciled": {"a": 1},
    "confidence_basis": {"score": 0.9},
    "lineage": {"stages": [{"stage": "a"}, {"stage": "b"}, {"stage": "c"}]},
    "narrative_monopoly_suppressed": True,
    "cognitive_decentralization": {"dominance_without_evidence": True},
    "semantic_decentralization": {"hierarchy_lock_in": True},
}

B = []


def fx(i, fn, args, kwargs=None):
    f = {"id": i, "fn": fn, "args": args}
    if kwargs:
        f["kwargs"] = kwargs
    B.append(f)


fx("c-astir-src", "compile_semantic_ast_ir", [PY_SRC])
fx("c-astir-empty", "compile_semantic_ast_ir", [""])
fx("c-coref-text", "build_coreference_graph", [COREF_TEXT])
fx("c-coref-plain", "build_coreference_graph", ["plain text, nothing else"])
fx("c-instr-steps", "analyze_instructional_semantics", [INSTR_TEXT])
fx("c-instr-empty", "analyze_instructional_semantics", [""])
fx("c-discourse-doc", "parse_semantic_discourse", [INSTR_TEXT])
fx("c-discourse-empty", "parse_semantic_discourse", [""])
fx("c-topo-cycle", "reason_topology_semantic",
   [{"nodes": [{"kind": "a"}, {"kind": "b"}],
     "edges": [{"from": "a", "to": "b"}, {"from": "b", "to": "a"}]}])
fx("c-topo-empty", "reason_topology_semantic", [{}])
fx("c-deploy-hits", "analyze_deployment_semantics",
   [["src\\Dockerfile", "k8s/deploy.yaml", "README.md",
     ".github/workflows/ci.yml", "helm/chart.yaml"]])
fx("c-deploy-none", "analyze_deployment_semantics", [["a.py", "b.md"]])

fx("c-integrity-full", "apply_cognitive_integrity", [B_FULL])
fx("c-integrity-empty", "apply_cognitive_integrity", [{}])
fx("c-integrity-allowed", "apply_cognitive_integrity",
   [{"evidence": ["e1", "e2", "e3"], "observed": {"i1": 1},
     "inferred": {"i1": 1}, "confidence_basis": {"score": 0.6}}])

fx("c-foundation-full", "apply_formal_semantic_foundation", [dict(B_FULL)])
fx("c-foundation-empty", "apply_formal_semantic_foundation", [{}])
fx("c-foundation-alt", "apply_formal_semantic_foundation",
   [{"contradictions": {"pairs": [["p", "q"], ["r", "s"]]},
     "evidence": ["e1", "e2"], "deterministic_inputs": ["seed=1"],
     "lineage": {"stages": [{"stage": "z"}]}}])

fx("c-openness-grav", "apply_civilizational_epistemic_openness",
   [dict(B_SOVEREIGN)])
fx("c-openness-diverse", "apply_civilizational_epistemic_openness",
   [dict(B_DIVERSE)])
fx("c-openness-empty", "apply_civilizational_epistemic_openness", [{}])
fx("c-openness-dictunc", "apply_civilizational_epistemic_openness",
   [dict(B_FULL)])

fx("c-capture-lockin", "apply_cognitive_anti_capture", [dict(B_SOVEREIGN)])
fx("c-capture-diverse", "apply_cognitive_anti_capture", [dict(B_DIVERSE)])
fx("c-capture-empty", "apply_cognitive_anti_capture", [{}])

fx("c-stability-full", "apply_epistemic_civilization_stability", [dict(B_FULL)])
fx("c-stability-diverse", "apply_epistemic_civilization_stability",
   [dict(B_DIVERSE)])
fx("c-stability-empty", "apply_epistemic_civilization_stability", [{}])

fx("c-sovereign-dep", "apply_recursive_epistemic_sovereignty",
   [dict(B_SOVEREIGN)])
fx("c-sovereign-indep", "apply_recursive_epistemic_sovereignty",
   [dict(B_DIVERSE)])
fx("c-sovereign-empty", "apply_recursive_epistemic_sovereignty", [{}])

fx("c-reality-plain", "apply_reality_bounded_confidence", [0.8, {}])
fx("c-reality-full", "apply_reality_bounded_confidence",
   [0.9, {"confidence_limits": {"max": 0.7}}],
   {"drift_pressure": 0.6, "continuity_count": 2, "parser_gap": True,
    "boundary_pressure": 0.4, "contradiction_count": 1, "ambiguity_count": 1,
    "uncertainty_count": 2})
fx("c-reality-partial", "apply_reality_bounded_confidence", [0.5, {}],
   {"drift_pressure": 0.3})

fx("c-collectspec-gap", "collect_suppressed_speculation",
   [["e1"], {"i1": 1, "i2": 2}, {"r": 1}])
fx("c-collectspec-ok", "collect_suppressed_speculation",
   [["e1", "e2"], {"i": 1}, {}])
fx("c-collectcont-gap", "collect_unsupported_continuity",
   [["e1"], {"i1": 1, "i2": 2}, {"r": 1}])
fx("c-collectcont-ok", "collect_unsupported_continuity",
   [["e1", "e2"], {"i": 1}, {}])

path = os.path.join(D, "fixtures.json")
existing = json.load(open(path, encoding="utf-8-sig"))
ids = {f["id"] for f in existing}
new_ids = {f["id"] for f in B}
assert not ids & new_ids, f"id collision: {ids & new_ids}"
merged = existing + B
with open(path, "w", encoding="utf-8") as fh:
    json.dump(merged, fh, ensure_ascii=False, indent=1)
print(f"added {len(B)} Phase C fixtures -> {len(merged)} total")
