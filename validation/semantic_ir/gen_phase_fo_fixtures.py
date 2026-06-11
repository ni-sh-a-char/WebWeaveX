"""One-shot generator: append the Phase F-O (document side) fixture set."""
import json
import os

D = os.path.dirname(os.path.abspath(__file__))

DOC = ("# Setup guide\nThis is because of reasons. It matters.\n\n"
       "## Step one: install\n- item alpha\n\n## Step two: verify\n"
       "Therefore we conclude. This builds on the engine.\n\n"
       "### Deep dive\nFor instance, an example.\n")

NUMBERED = "intro text\n1. first step\n2. second step\n3. third step\n"

RRI_DEEP = {
    "evidence": ["e1"],
    "ambiguities": ["amb1"],
    "uncertainties": {"u1": 1},
    "inferred": {"a": 1},
    "reconciled": {"a": 1},
    "contradicted": {"pairs": [["x", "y"]]},
    "lineage": {"stages": [{"stage": "a"}, {"stage": "b"}, {"stage": "c"}]},
    "sources": ["src1"],
    "confidence_basis": {"score": 0.9},
}

RRI_INSTAB = {
    "evidence": ["e1", "e2"],
    "uncertain": ["u-list"],
    "inferred": {"a": 1, "b": 2},
    "reconciled": {},
    "instability": {"regions": ["zone1"]},
    "fragility": "notadict",
    "lineage": {"depth": 2, "stages": []},
}

ATTACH_FULL = {
    "evidence": ["e1"],
    "ambiguities": ["amb1"],
    "observed": {"o1": 1},
    "inferred": {"i1": 1},
    "reconciled": {"i1": 1},
    "contradicted": {"pairs": [["x", "y"]], "preserved": True},
    "parser_basis": {"symbol_count": 2, "flags": {"ast": True}},
    "lineage": {"stages": [{"stage": "s1"}], "depth": 1},
    "confidence_basis": {"score": 0.8},
}

PARSER_PAYLOAD = {
    "language": "python",
    "parser_evidence": {"ast": True, "symbols": True, "imports": False},
    "symbols": {"classes": ["A", "B"], "functions": ["f"], "imports": ["os"]},
}

B = []


def fx(i, fn, args, kwargs=None):
    f = {"id": i, "fn": fn, "args": args}
    if kwargs:
        f["kwargs"] = kwargs
    B.append(f)


fx("f-progress-doc", "model_concept_progression", [DOC])
fx("f-progress-empty", "model_concept_progression", [""])
fx("f-rri-deep", "apply_recursive_reality_integrity", [RRI_DEEP])
fx("f-rri-instab", "apply_recursive_reality_integrity", [RRI_INSTAB])
fx("f-rri-empty", "apply_recursive_reality_integrity", [{}])
fx("g-attach-full", "attach_epistemic_state", [ATTACH_FULL])
fx("g-attach-empty", "attach_epistemic_state", [{}])
fx("h-bsio-min", "build_semantic_integrity_object", [])
fx("h-bsio-full", "build_semantic_integrity_object",
   [{"o1": 1}, {"language": "python"}, {"i1": 1}, {"i1": 1},
    {"pairs": [["p", "q"]]}, {"structure": "x"}, ["amb1", "amb1", "amb2"],
    PARSER_PAYLOAD,
    [{"stage": "parse", "inputs": [], "outputs": ["parser:ast"]}]])
fx("i-uncertain-full", "apply_semantic_uncertainty",
   [{"evidence": ["e1"], "ambiguities": ["a1"],
     "contradicted": {"pairs": [["x", "y"]]},
     "confidence_basis": {"score": 0.9}}])
fx("i-uncertain-empty", "apply_semantic_uncertainty", [{}])
fx("i-structure-plain", "structure_cognition",
   [{"o": 1}, {"i": 1}, {"o": 1, "i": 1}])
fx("i-structure-parsed", "structure_cognition",
   [{"o": 1}, {"i": 1}, {"r": 2}, PARSER_PAYLOAD,
    {"pairs": [["a", "b"]]}, ["ambX"]])
fx("i-structure-inferonly", "structure_cognition", [{}, {"i": 1}, {}])
fx("j-tutflow-doc", "extract_tutorial_flow", [DOC])
fx("j-tutflow-numbered", "extract_tutorial_flow", [NUMBERED])
fx("j-tutflow-empty", "extract_tutorial_flow", [""])
fx("k-tutdep-doc", "reconstruct_tutorial_dependencies", [DOC])
fx("l-tutprereq-doc", "infer_tutorial_prerequisites", [DOC])
fx("m-docir-doc", "build_document_semantic_ir", [DOC])
fx("m-docir-empty", "build_document_semantic_ir", [""])
fx("n-longrange-doc", "analyze_long_range_discourse", [DOC])
fx("n-compile-doc", "compile_document_ir", [DOC])
fx("n-compile-empty", "compile_document_ir", [""])
fx("o-query-doc", "query_documents", [DOC])
fx("o-discourse-doc", "reason_discourse_semantic", [DOC])

path = os.path.join(D, "fixtures.json")
existing = json.load(open(path, encoding="utf-8-sig"))
ids = {f["id"] for f in existing}
assert not ids & {f["id"] for f in B}
merged = existing + B
with open(path, "w", encoding="utf-8") as fh:
    json.dump(merged, fh, ensure_ascii=False, indent=1)
print(f"added {len(B)} Phase F-O fixtures -> {len(merged)} total")
