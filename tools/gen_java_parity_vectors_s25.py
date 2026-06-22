#!/usr/bin/env python3
"""Session-25 cross-language golden vectors from canonical Python 2.1.0.

    python tools/gen_java_parity_vectors_s25.py <out.json>

Covers run_semantic_runtime + run_semantic_for_extraction (portable html="" contract) and the
pure semantic sub-engines. Python is the oracle. Every vector uses html="" so the output is
bs4-independent.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.semantic.semantic_orchestrator import run_semantic_runtime, run_semantic_for_extraction
from core.semantic.entity_extraction_engine import extract_semantic_entities
from core.semantic.entity_resolution_engine import resolve_semantic_entities
from core.semantic.domain_classification_engine import classify_semantic_domain
from core.semantic.ontology_engine import build_semantic_ontology
from core.semantic.semantic_graph_engine import build_semantic_graph
from core.semantic.document_semantics_engine import extract_document_semantics
from core.semantic.table_semantics_engine import extract_table_semantics
from core.semantic.ui_semantics_engine import extract_ui_semantics
from core.semantic.repository_semantics_engine import extract_repository_semantics
from core.semantic.application_semantics_engine import extract_application_semantics
from core.semantic.causality_semantics_engine import extract_causality_semantics
from core.semantic.workflow_semantics_engine import extract_workflow_semantics
from core.semantic.browser_semantics_engine import extract_browser_semantics
from core.semantic.runtime_semantics_engine import extract_runtime_semantics
from core.semantic.semantic_alignment_engine import align_semantic_runtimes
from core.semantic.semantic_diff_engine import diff_semantic_runtime


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


APP = {"workflow": {"nodes": [{"n": 1}], "edges": [{"e": 1}]}, "execution": {"objective": "op",
        "executed": [{"action": "click"}]}, "intent": {"intent": "manage"}, "forms": {"forms": [{"f": 1}]},
       "ui_semantics": {"a": 1}}
CAUS = {"causality": {"propagation": {"handoffs": [{"from": "a", "to": "b"}]}, "alignment": {"runtime_count": 2}}}
RG = {"nodes": [{"id": "n1"}, {"id": "n2"}], "edges": [{"from": "n1", "to": "n2"}]}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 25: semantic runtime, html='' contract)"}

    runs = [
        ("empty", dict(html="")),
        ("text", dict(html="", text="User logs into the dashboard. The API service deploys to kubernetes.",
                      objective="extract", interactions=[{"action": "click"}, {"action": "fill"}])),
        ("rich", dict(html="", text="Invoice billing payment. CRM customer lead.", objective="monitor",
                      application_result=APP, causality_result=CAUS, runtime_graph=RG,
                      native_cognition={"runtime": "electron"}, repository_files=["api/routes.py", "Dockerfile"],
                      interactions=[{"action": "submit"}])),
        ("memory", dict(html="", text="user account", memory={"entities": {"entities": [{"id": "old"}]},
                        "domain": {"domain": "saas"}})),
    ]
    out["run_semantic_runtime"] = [ev(n, {**kw}, run_semantic_runtime(**kw)) for n, kw in runs]

    rfe = [
        ("disabled", dict(semantic_runtime=False)),
        ("default", dict(html="", objective="extract", interactions=[{"action": "click"}])),
        ("no_merge", dict(html="", application_result=APP, runtime_graph=RG, merge_graph=False)),
    ]
    out["run_semantic_for_extraction"] = [ev(n, {**kw}, run_semantic_for_extraction(**kw)) for n, kw in rfe]

    # ---- engine-level parity ----
    TEXTS = ["", "User API service workflow kubernetes deploy", "Invoice billing ledger payment dashboard kpi"]
    out["extract_semantic_entities"] = [
        ev("ent_" + str(i), {"text": t, "structure": {"actions": [{"label": "click"}], "artifacts": ["rt"]}},
           extract_semantic_entities(t, {"actions": [{"label": "click"}], "artifacts": ["rt"]}))
        for i, t in enumerate(TEXTS)
    ]
    ENTS = extract_semantic_entities("User API service", {"actions": [{"label": "x"}]})["entities"]
    out["resolve_semantic_entities"] = [ev("resolve", {"entities": ENTS}, resolve_semantic_entities(ENTS))]
    out["classify_semantic_domain"] = [
        ev("dom_" + str(i), {"text": t, "signals": ["extract"]}, classify_semantic_domain(t, ["extract"]))
        for i, t in enumerate(TEXTS)
    ]
    out["build_semantic_ontology"] = [ev("onto", {"entities": ENTS, "domain": "saas"},
                                         build_semantic_ontology(ENTS, "saas"))]
    RELS = extract_semantic_entities("User API service", {})["relations"]
    out["build_semantic_graph"] = [
        ev("graph", {"entities": ENTS, "relations": RELS}, build_semantic_graph(ENTS, RELS)),
        ev("graph_empty", {"entities": [], "relations": []}, build_semantic_graph([], [])),
    ]
    out["extract_document_semantics"] = [ev("doc_" + str(i), {"text": t}, extract_document_semantics(t))
                                         for i, t in enumerate(TEXTS + ["agreement terms party architecture module"])]
    out["extract_table_semantics"] = [ev("tbl_empty", {"html": ""}, extract_table_semantics(""))]
    out["extract_ui_semantics"] = [
        ev("ui_empty", {"actions": []}, extract_ui_semantics("", [])),
        ev("ui_actions", {"actions": [{"action": "click"}, {"action": "fill"}]},
           extract_ui_semantics("", [{"action": "click"}, {"action": "fill"}])),
    ]
    out["extract_repository_semantics"] = [
        ev("repo", {"files": ["api/routes.py", "docker-compose.yml"], "text": "service worker"},
           extract_repository_semantics(["api/routes.py", "docker-compose.yml"], "service worker")),
        ev("repo_docs", {"files": [], "text": "docs readme"}, extract_repository_semantics([], "docs readme")),
    ]
    out["extract_application_semantics"] = [
        ev("app", {"application_result": APP}, extract_application_semantics(APP)),
        ev("app_empty", {"application_result": None}, extract_application_semantics(None)),
    ]
    out["extract_causality_semantics"] = [
        ev("caus", {"causality_result": CAUS}, extract_causality_semantics(CAUS)),
        ev("caus_empty", {"causality_result": None}, extract_causality_semantics(None)),
    ]
    out["extract_workflow_semantics"] = [
        ev("wf", {"workflow": {"nodes": [1, 2], "edges": [1]}, "objective": "op"},
           extract_workflow_semantics({"nodes": [1, 2], "edges": [1]}, "op")),
        ev("wf_empty", {"workflow": None, "objective": ""}, extract_workflow_semantics(None, "")),
    ]
    out["extract_browser_semantics"] = [ev("browser", {"url": "https://x", "html": ""},
                                           extract_browser_semantics("https://x", ""))]
    out["extract_runtime_semantics"] = [
        ev("rt", {"runtime_graph": RG, "sources": {"browser": True, "native": False}},
           extract_runtime_semantics(RG, {"browser": True, "native": False})),
    ]
    BR = extract_browser_semantics("https://x", "")
    out["align_semantic_runtimes"] = [
        ev("align", {"browser": {**BR, "domain": "saas"}, "repository": {"repository_purpose": "application"}},
           align_semantic_runtimes(browser={**BR, "domain": "saas"},
                                    repository={"repository_purpose": "application"})),
    ]
    out["diff_semantic_runtime"] = [
        ev("diff", {"previous": {"entities": {"entities": [{"id": "a"}]}, "domain": {"domain": "saas"}},
                    "current": {"entities": {"entities": [{"id": "b"}]}, "domain": {"domain": "crm"}}},
           diff_semantic_runtime({"entities": {"entities": [{"id": "a"}]}, "domain": {"domain": "saas"}},
                                 {"entities": {"entities": [{"id": "b"}]}, "domain": {"domain": "crm"}})),
    ]

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s25.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors across {len(counts)} sections\n")


if __name__ == "__main__":
    main()
