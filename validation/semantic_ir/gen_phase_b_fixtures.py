"""One-shot generator: append the Phase B fixture set to fixtures.json."""
import json
import os

D = os.path.dirname(os.path.abspath(__file__))

PY_SIMPLE = (
    "import os\nimport sys as system\n\ndef main(a, b=1):\n    return a\n\n"
    "class Foo(Base):\n    def method(self):\n        pass\n\n"
    "class Bar:\n    pass\n\nx = 5\ny = compute(1, 2)\n"
)
PY_FROM = (
    "from typing import Any, Dict\nfrom os.path import (join,\n    split)\n\n\n"
    "def solo():\n    inner = 1\n    return inner\n"
)
# NOTE: `async def` is intentionally absent here. CPython's ast.walk collects
# ast.FunctionDef only (async def -> ast.AsyncFunctionDef), but the JS branch's
# scanner matches `(?:async\s+)?def` and wrongly emits a FunctionDef — a
# JS-branch divergence from canonical Python (see SEMANTIC_IR_PARITY_REPORT.md).
# The async case is proven Python ≡ Dart by an executed-Python vector in
# test/parity/semantic_ir_b_test.dart instead.
PY_DECORATED = (
    "import json, re\n\n@decorator\ndef fetch(url):\n"
    "    data = get(url)\n    return data\n\nresult = fetch('x')\n"
)
PY_NESTED = (
    "def outer(a):\n    first = a\n    def inner(b):\n        second = b\n"
    "        return second\n    return inner\n\nlast = outer(1)\n"
)

DOC_TEXT = (
    "# Intro\nThis is because of reasons.\n\n## Step one: install\n"
    "- item alpha\n- item beta\n\n## Background\nTherefore we conclude.\n\n"
    "### Deep dive\nFor instance, an example.\n\n# Intro\n```\ncode here\n```\n"
)
DOC_SHORT = "# Only heading\nplain line\n"

B = []


def fx(i, fn, args, kwargs=None):
    f = {"id": i, "fn": fn, "args": args}
    if kwargs:
        f["kwargs"] = kwargs
    B.append(f)


# ast
fx("b-ast-simple", "parse_python_ast", [PY_SIMPLE])
fx("b-ast-from", "parse_python_ast", [PY_FROM])
fx("b-ast-decorated", "parse_python_ast", [PY_DECORATED])
fx("b-ast-nested", "parse_python_ast", [PY_NESTED])
fx("b-ast-empty", "parse_python_ast", [""])

# documents
fx("b-argdep-multi", "build_argument_dependencies",
   ["Claim one.\nClaim two.\n\n  Claim three.  \n"])
fx("b-argdep-single", "build_argument_dependencies", ["Only claim."])
fx("b-argdep-empty", "build_argument_dependencies", [""])
fx("b-arggraph-multi", "build_argument_graph", [DOC_TEXT])
fx("b-arggraph-one", "build_argument_graph", [DOC_SHORT])
fx("b-arggraph-none", "build_argument_graph", ["no headings here\njust text\n"])
fx("b-iflow-mixed", "extract_instructional_flow", [DOC_TEXT])
fx("b-iflow-none", "extract_instructional_flow", ["### Too deep\nplain\n"])
fx("b-iflow-keywords", "extract_instructional_flow",
   ["#### Setup prerequisites\n## Tutorial part\n# Overview\n"])
fx("b-rhetparse-mixed", "parse_rhetorical_structure", [DOC_TEXT])
fx("b-rhetparse-plain", "parse_rhetorical_structure",
   ["just a line\nanother because line\n"])
fx("b-rhetparse-empty", "parse_rhetorical_structure", [""])
fx("b-sections-dup", "extract_sections", [DOC_TEXT])
fx("b-sections-levels", "extract_sections", ["# Z\n## A\n### M\n"])
fx("b-sections-empty", "extract_sections", [""])

# evidence
fx("b-confdeg-plain", "apply_confidence_degradation", [0.8, {}])
fx("b-confdeg-full", "apply_confidence_degradation",
   [0.9, {"confidence_limits": {"max": 0.7}}],
   {"contradiction_count": 1, "ambiguity_count": 2, "uncertainty_count": 3,
    "speculation_count": 1, "parser_weakness": True})
fx("b-confdeg-floor", "apply_confidence_degradation", [0.3, {}],
   {"speculation_count": 5, "uncertainty_count": 10})
fx("b-reasondet-suff", "reason_deterministically", [{"a": 1}, ["e1", "e2"], []])
fx("b-reasondet-insuff", "reason_deterministically", [{"a": 1}, ["e1"], ["amb"]])
fx("b-reasondet-empty", "reason_deterministically", [{}, [], []])
fx("b-epconf-ev", "score_epistemic_confidence", [["e1", "e2", "e3"]])
fx("b-epconf-mixed", "score_epistemic_confidence",
   [["e1"], None, ["c1", "c2"], ["u1"], 3])
fx("b-epconf-empty", "score_epistemic_confidence", [[], [], [], [], 0])
fx("b-epconf-cap", "score_epistemic_confidence", [["e1", "e2"], ["s1"], [], [], 10])
fx("b-incomp-empty", "preserve_incompleteness", [{}])
fx("b-incomp-amb", "preserve_incompleteness",
   [{"evidence": ["e"], "ambiguities": ["a1", "a2"],
     "contradicted": {"preserved": True}}])
fx("b-incomp-pairs", "preserve_incompleteness",
   [{"evidence": ["e"], "observed": {"x": 1}, "parsed": {"y": 2},
     "reconciled": {"z": 3}, "contradicted": {"pairs": [["a", "b"]]}}])
fx("b-inflim-allowed", "model_inference_limits", [{"k1": 1, "k2": 2}, 3])
fx("b-inflim-blocked", "model_inference_limits", [{"k": 1}, 1])
fx("b-valinf-ok", "validate_inference", [{"a": 1}, ["e1"]])
fx("b-valinf-empty", "validate_inference", [{}, []])
fx("b-reality-grow", "apply_reality_constraints", [["e1", "e2"], True, 0.1])
fx("b-reality-drift", "apply_reality_constraints", [["e1"], False, 0.5])
fx("b-reality-edge", "apply_reality_constraints", [[], True, 0.29])
fx("b-recdep-y", "detect_recursive_dependency", [3, 1, 1])
fx("b-recdep-n", "detect_recursive_dependency", [1, 5, 5])
fx("b-recclose-coh", "detect_recursive_semantic_closure",
   [2, {"a": 1}, {"a": 1}, []])
fx("b-recclose-amp", "detect_recursive_semantic_closure",
   [3, {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7}, {}, ["e"]])
fx("b-recclose-n", "detect_recursive_semantic_closure",
   [1, {}, {}, ["e1", "e2"]])
fx("b-attractor-y", "detect_semantic_attractor", [2, 1, 0])
fx("b-attractor-n", "detect_semantic_attractor", [5, 3, 4])
fx("b-ground-parser", "_ground_parser",
   [{"language": "python",
     "parser_evidence": {"ast": True, "imports": False, "symbols": True},
     "symbols": {"classes": ["A"], "functions": ["f", "g"]}}])
fx("b-ground-evfallback", "_ground_parser", [{"evidence": {"b": 1, "a": 0}}])
fx("b-ground-nondict", "_ground_parser",
   [{"parser_evidence": "notadict", "symbols": "alsonot"}])
fx("b-monoc-y", "detect_semantic_monoculture", [[{"i": 1}], [], 2])
fx("b-monoc-n", "detect_semantic_monoculture", [[{"i": 1}, {"j": 2}], ["e"], 3])
fx("b-monop-y", "detect_semantic_monopoly", [1, 2, 1])
fx("b-monop-n", "detect_semantic_monopoly", [4, 2, 5])
fx("b-reliab-clean", "score_reliability", [["e1", "e2"], []])
fx("b-reliab-penalty", "score_reliability", [["e1"], ["a1", "a2"], 2])
fx("b-reliab-null", "score_reliability", [[], None, 0])
fx("b-restraint-empty", "apply_epistemic_restraint", [{}])
fx("b-restraint-full", "apply_epistemic_restraint",
   [{"evidence": ["e1"], "ambiguities": ["a"], "observed": {"o": 1},
     "inferred": {"i1": 1, "i2": 2, "i3": 3}, "reconciled": {},
     "contradicted": {"pairs": [["x", "y"]], "preserved": True},
     "confidence_basis": {"score": 0.8},
     "fragility": {"confidence_limits": {"max": 0.6}}}])
fx("b-restraint-alt", "apply_epistemic_restraint",
   [{"evidence": ["e1", "e2", "e3"], "inferred": {"a": 1},
     "contradictions": {"pairs": []}, "fragile": {"level": "low"},
     "boundaries": {"existing": True}}])
fx("b-propunc-empty", "propagate_uncertainty", [{}])
fx("b-propunc-pairs", "propagate_uncertainty",
   [{"evidence": ["e1", "e2"], "ambiguities": ["a1"],
     "contradicted": {"pairs": [["p", "q"], ["r", "s"]]}}])
fx("b-propunc-nondict", "propagate_uncertainty",
   [{"evidence": ["e"], "contradicted": "notadict"}])
fx("b-spec-clean", "suppress_speculative_inference", ["x", ["e1", "e2"]])
fx("b-spec-inferred", "suppress_speculative_inference", ["claim", []],
   {"inferred": True})
fx("b-spec-high", "suppress_speculative_inference", ["deep", ["e1"]],
   {"inferred": True, "min_evidence": 3, "fragility_level": "high"})
fx("b-uncmath-default", "propagate_uncertainty_math", [2, 1, 0])
fx("b-uncmath-parent", "propagate_uncertainty_math", [0, 2, 1, 0.4])
fx("b-uncmath-low", "propagate_uncertainty_math", [5, 0, 0, 0.25])
fx("b-cont-y", "suppress_unsupported_continuity", ["s1", []])
fx("b-cont-n", "suppress_unsupported_continuity", ["s2", ["e1", "e2"]])
fx("b-cont-kw", "suppress_unsupported_continuity", ["s3", ["e1"]],
   {"min_evidence": 3})
fx("b-stab-coh", "detect_unsupported_stabilization", [[], {"a": 1}, {"a": 1}])
fx("b-stab-amp", "detect_unsupported_stabilization", [[], {"a": 1, "b": 2}, {}])
fx("b-stab-n", "detect_unsupported_stabilization",
   [["e1", "e2"], {"a": 1}, {"a": 1}])
fx("b-stab-kw", "detect_unsupported_stabilization",
   [["e1"], {"a": 1, "b": 2, "c": 3}, {"x": 9}], {"min_evidence": 2})

# graph / ir / repository / semantic
fx("b-topo-hub", "reason_topology",
   [{"nodes": [{"kind": "a"}, {"kind": "b"}],
     "edges": [{"from": "h", "to": "a"}, {"from": "h", "to": "b"},
               {"from": "c", "to": "h"}]}])
fx("b-topo-empty", "reason_topology", [{}])
fx("b-topo-mixed", "reason_topology",
   [{"nodes": [{"kind": "a"}, {"kind": "a"}, "raw"],
     "edges": [{"from": "x", "to": "y"}]}])
fx("b-docir-empty", "empty_document_ir", [])
fx("b-repoir-empty", "empty_repository_ir", [])
fx("b-apicontract-paths", "reason_api_contract",
   [{"paths": {"/users": {"get": {}, "post": {}}, "/health": {"delete": {}}}}])
fx("b-apicontract-empty", "reason_api_contract", [{}])
fx("b-infrarel-hits", "model_infra_relationships",
   [["src\\Dockerfile", "k8s/deploy.yaml", "README.md",
     ".github/workflows/ci.yml", "infra/terraform/main.tf"]])
fx("b-infrarel-none", "model_infra_relationships", [["a.py", "b.md"]])
fx("b-contrarestraint-pairs", "apply_contradiction_restraint",
   [{"contradicted": {"pairs": [["a", "b"]]}}])
fx("b-contrarestraint-alt", "apply_contradiction_restraint",
   [{"contradictions": {"pairs": []}, "fragility_pressure": {"base": 0.2}}])
fx("b-contrarestraint-empty", "apply_contradiction_restraint", [{}])

path = os.path.join(D, "fixtures.json")
existing = json.load(open(path, encoding="utf-8-sig"))
ids = {f["id"] for f in existing}
new_ids = {f["id"] for f in B}
assert not ids & new_ids, f"id collision: {ids & new_ids}"
merged = existing + B
with open(path, "w", encoding="utf-8") as fh:
    json.dump(merged, fh, ensure_ascii=False, indent=1)
print(f"added {len(B)} Phase B fixtures -> {len(merged)} total")
