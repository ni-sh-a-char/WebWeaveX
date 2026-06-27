#!/usr/bin/env python3
"""Session-36 Repository-IR golden vectors from canonical Python 2.1.0.

Certifies the ENTIRE repository-IR layer + the three public APIs that bottom out at
compile_repository_ir, byte-exact vs canonical Python:
  - compile_repository(source, path)
  - query_semantics("repository", {source, path})       (core.query.repository_query_engine path)
  - reason_semantically("runtime", {source, path})       (core.reasoning.runtime_reasoning_engine path)

Plus per-engine vectors (Phase 8) for every engine in the runtime closure. The epistemic
normalize_parser_output is discarded by the repository layer (proven: repository engines read only
parsed.{language,symbols,calls,dependencies,runtime,parser_grounding,evidence}) and is not exercised.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

# IR + base
from core.ir._base import empty_confidence, empty_lineage, merge_evidence
from core.ir.repository_ir import compile_repository_ir, empty_repository_ir
from core.ir.semantic_query_ir import compile_semantic_query_ir
# repository engines (full closure)
from core.repository.runtime_dependency_engine import resolve_runtime_dependencies
from core.repository.execution_flow_engine import reconstruct_execution_flow
from core.repository.service_interaction_engine import infer_service_interactions
from core.repository.runtime_semantics_engine import analyze_runtime_semantics
from core.repository.execution_dependency_engine import model_execution_dependencies
from core.repository.runtime_flow_reasoner import reason_runtime_flow
from core.repository.service_runtime_graph_engine import build_service_runtime_graph
from core.repository.infra_semantic_engine import detect_infra_signals
from core.repository.infra_relationship_engine import model_infra_relationships
from core.repository.deployment_semantics_engine import analyze_deployment_semantics
from core.repository.api_surface_reasoning_engine import reason_api_surface
from core.repository.api_contract_reasoning_engine import reason_api_contract
from core.repository.repository_semantic_ir_engine import build_repository_semantic_ir
from core.repository.repository_execution_ir_engine import build_repository_execution_ir
from core.repository.runtime_execution_engine import analyze_runtime_execution
from core.repository.runtime_state_engine import model_runtime_state
# public dispatch leaves
from core.query.repository_query_engine import query_repository
from core.reasoning.runtime_reasoning_engine import reason_runtime_semantic
# parser helper to construct `parsed` for engine-level vectors
from core.parsers.parser_registry import parse_source


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


# --- source corpus (text contract: empty path -> language="text"; + python-path probes) -----------
SRC_PY = "import os\nimport sys\ndef main():\n    helper()\n    return run_job()\ndef helper():\n    pass\ndef run_job():\n    return 1\nclass Worker(Base):\n    def step(self):\n        return self.x\n"
SRC_REQS = "flask==2.0\nrequests>=2.0\nnumpy\n# comment\n"
SRC_PROSE = "this is just documentation text\nno code here\n"
SRC_EMPTY = ""
SRC_JS = "import x from 'y'\nfunction handler(req) {\n  return doWork(req)\n}\n"

FILES_INFRA = ["docker-compose.yml", "k8s/deployment.yaml", "src/main.py", ".github/workflows/ci.yml"]
OPENAPI = {"paths": {"/users": {"get": {}, "post": {}}, "/items/{id}": {"delete": {}}}}

# PORTABLE contract cases: (name, source, path). resolve_symbols/build_call_graph only special-case
# language=="python"; EVERY other language (text/js/ts/java/go/rust) takes the regex path (S34, byte-
# exact). So these cases are fully portable with NO CPython dependency.
CASES = [
    ("py_text", SRC_PY, ""),            # path="" => language="text" (regex)
    ("reqs_text", SRC_REQS, ""),
    ("prose", SRC_PROSE, ""),
    ("empty", SRC_EMPTY, ""),
    ("js_text", SRC_JS, ""),
    ("js_dot_js", SRC_JS, "app.js"),    # language="javascript" => regex path (still portable)
    ("py_as_ts", SRC_PY, "x.ts"),       # language="typescript" => regex path (NOT python)
]
# compile_repository_ir calls compile_semantic_ast_ir(source) UNCONDITIONALLY. CPython ast.parse
# raises SyntaxError on non-python source (=> {semantic_grounded: False}); the S33 line-scanner is
# more lenient. So the semantic_ast field (and thus the 3 public APIs) is byte-exact only for sources
# that are VALID PYTHON. The 14-engine layer below is byte-exact for ALL sources (no semantic_ast).
VALID_PY_CASES = [c for c in CASES if c[0] in ("py_text", "reqs_text", "empty", "py_as_ts")]

# RESIDUALS recorded for evidence, NOT asserted by Java this session:
#  - python (.py) path: resolve_symbols/build_call_graph take CPython ast (symbols=7 vs 5, caller attr).
#  - invalid-python source: S33 scanner accepts what CPython rejects (semantic_ast diverges).
PYTHON_PROBE = [("py_dot_py", SRC_PY, "worker.py")]
INVALID_PY_PROBE = [("js_text", SRC_JS, ""), ("prose", SRC_PROSE, "")]


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 36: repository IR layer + public APIs)"}

    # ---- IR base helpers
    out["merge_evidence"] = [
        ev("dup_sort", {"parts": [["b", "a", "a", ""], ["c", "a"]]}, merge_evidence(["b", "a", "a", ""], ["c", "a"])),
        ev("empty", {"parts": [[]]}, merge_evidence([])),
    ]
    out["empty_confidence"] = [ev("const", {}, empty_confidence())]
    out["empty_lineage"] = [ev("repo", {"stage": "repository_ir"}, empty_lineage("repository_ir"))]
    out["empty_repository_ir"] = [ev("const", {}, empty_repository_ir())]

    # ---- per-engine vectors over the corpus (Phase 8: every engine)
    def parsed_of(s, p):
        return parse_source(s, path=p) if s else {}

    out["resolve_runtime_dependencies"] = [
        ev(n, {"source": s, "path": p}, resolve_runtime_dependencies(parsed_of(s, p), s)) for n, s, p in CASES
    ]
    out["reconstruct_execution_flow"] = [
        ev(n, {"source": s, "path": p}, reconstruct_execution_flow(parsed_of(s, p))) for n, s, p in CASES
    ]
    out["infer_service_interactions"] = [
        ev(n, {"source": s, "path": p}, infer_service_interactions(parsed_of(s, p), FILES_INFRA)) for n, s, p in CASES
    ]
    out["analyze_runtime_semantics"] = [
        ev(n, {"source": s, "path": p}, analyze_runtime_semantics(s, p)) for n, s, p in CASES
    ]
    out["model_execution_dependencies"] = [
        ev(n, {"source": s, "path": p}, model_execution_dependencies(s, p)) for n, s, p in CASES
    ]
    out["reason_runtime_flow"] = [
        ev(n, {"source": s, "path": p}, reason_runtime_flow(s, p)) for n, s, p in CASES
    ]
    out["build_service_runtime_graph"] = [
        ev(n, {"source": s, "path": p}, build_service_runtime_graph(s, p)) for n, s, p in CASES
    ]
    out["detect_infra_signals"] = [
        ev("infra", {"files": FILES_INFRA}, detect_infra_signals(FILES_INFRA)),
        ev("none", {"files": ["a.py", "b.js"]}, detect_infra_signals(["a.py", "b.js"])),
        ev("empty", {"files": []}, detect_infra_signals([])),
    ]
    out["model_infra_relationships"] = [
        ev("infra", {"files": FILES_INFRA}, model_infra_relationships(FILES_INFRA)),
        ev("none", {"files": ["a.py"]}, model_infra_relationships(["a.py"])),
    ]
    out["analyze_deployment_semantics"] = [
        ev("infra", {"files": FILES_INFRA}, analyze_deployment_semantics(FILES_INFRA)),
        ev("none", {"files": ["a.py", "b.js"]}, analyze_deployment_semantics(["a.py", "b.js"])),
        ev("empty", {"files": []}, analyze_deployment_semantics([])),
    ]
    out["reason_api_surface"] = [
        ev("openapi", {"spec": OPENAPI}, reason_api_surface(OPENAPI)),
        ev("empty", {"spec": {}}, reason_api_surface({})),
    ]
    out["reason_api_contract"] = [
        ev("openapi", {"spec": OPENAPI}, reason_api_contract(OPENAPI)),
    ]
    out["analyze_runtime_execution"] = [
        ev(n, {"source": s, "path": p}, analyze_runtime_execution(s, p)) for n, s, p in CASES
    ]
    out["model_runtime_state"] = [
        ev(n, {"source": s, "path": p}, model_runtime_state(s, p)) for n, s, p in CASES
    ]
    out["build_repository_semantic_ir"] = [
        ev(n, {"source": s, "path": p}, build_repository_semantic_ir(s, p)) for n, s, p in CASES
    ]
    out["build_repository_execution_ir"] = [
        ev(n, {"source": s, "path": p}, build_repository_execution_ir(s, p)) for n, s, p in CASES
    ] + [ev("openapi", {"source": SRC_PY, "path": "", "openapi": True},
            build_repository_execution_ir(SRC_PY, "", None, OPENAPI))]

    # ---- compile_repository_ir (the hub) + public APIs  (valid-python sources: semantic_ast matches)
    out["compile_repository_ir"] = [
        ev(n, {"source": s, "path": p}, compile_repository_ir(s, p)) for n, s, p in VALID_PY_CASES
    ] + [
        ev("with_files", {"source": SRC_PY, "path": "", "files": FILES_INFRA},
           compile_repository_ir(SRC_PY, "", FILES_INFRA)),
        ev("with_openapi", {"source": SRC_PY, "path": "", "openapi": True},
           compile_repository_ir(SRC_PY, "", None, OPENAPI)),
    ]

    # public: compile_repository(source, path) == compile_repository_ir(source, path, files)
    out["compile_repository"] = [
        ev(n, {"source": s, "path": p}, compile_repository_ir(s, p, None)) for n, s, p in VALID_PY_CASES
    ]
    # public: query_semantics("repository", {source, path}). target = str(payload)[:80] (Python dict
    # repr) is stored verbatim in inputs so the Java test need not reproduce CPython dict-repr.
    out["query_semantics_repository"] = [
        ev(n, {"source": s, "path": p, "target": str({"source": s, "path": p})[:80]},
           compile_semantic_query_ir("repository", str({"source": s, "path": p})[:80],
                                     query_repository(s, p)))
        for n, s, p in VALID_PY_CASES
    ]
    # public: reason_semantically("runtime", {source, path})
    out["reason_semantically_runtime"] = [
        ev(n, {"source": s, "path": p},
           {**reason_runtime_semantic(s, p), "domain": "runtime", "deterministic": True})
        for n, s, p in VALID_PY_CASES
    ]

    # residuals: recorded for evidence only (NOT asserted by Java this session)
    out["_python_contract_residual"] = [
        ev(n, {"source": s, "path": p, "note": "CPython ast branch — resolve_symbols + build_call_graph"},
           compile_repository_ir(s, p)) for n, s, p in PYTHON_PROBE
    ]
    out["_invalid_python_residual"] = [
        ev(n, {"source": s, "path": p, "note": "semantic_ast: CPython SyntaxError vs S33 lenient scanner"},
           compile_repository_ir(s, p)) for n, s, p in INVALID_PY_PROBE
    ]

    path = sys.argv[1] if len(sys.argv) > 1 else "repository_vectors_s36.json"
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    total = sum(len(v) for k, v in out.items() if isinstance(v, list))
    print(f"wrote {path} ({total} vectors across {sum(1 for v in out.values() if isinstance(v,list))} engines/APIs)")


if __name__ == "__main__":
    main()
