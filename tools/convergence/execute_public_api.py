#!/usr/bin/env python3
"""PHASE 7 — execute (not merely import) the Python public API and record
importable / callable / executed / deterministic per symbol. A curated input
map drives the core engines; a generic fallback attempts the rest. Honest:
symbols that genuinely need domain-specific args are recorded as
callable-but-not-auto-executed rather than faked.
"""
from __future__ import annotations

import json
import inspect
from datetime import datetime, timezone

import webweavex as w

GRAPH_IRS = [{"ir": "browser", "nodes": [{"id": "n1"}, {"id": "n2"}], "edges": [{"from": "n1", "to": "n2"}]}]
GRAPH = w.build_runtime_graph(GRAPH_IRS)
ENVELOPE = {"unified_runtime_graph": GRAPH, "browser_ir": {"runtime_identity": "id"}}
RESULT = {"content": {"repository": {}, "documents": {}}, "relationships": {"execution_graph": GRAPH}}

# curated argument tuples for functions that take meaningful inputs
CURATED = {
    "build_runtime_graph": (GRAPH_IRS,),
    "query_runtime_graph": (GRAPH, {}),
    "compute_global_runtime_fingerprint": ({"graph": GRAPH},),
    "compute_kaalka_hash": ("abc123",),
    "fingerprint": ("abc123",),
    "encrypt_value": ({"a": 1}, "key"),
    "build_runtime_memory": (GRAPH,),
    "build_interaction_graph": ([{"action": "click"}],),
    "build_workflow_plan": ([{"step": "a"}],),
    "build_stream_timeline": ([{"timestamp": 1, "id": "e"}],),
    "build_browser_identity": ({"user_agent": "x"},),
    "reason_semantically": ([{"label": "x"}],),
    "ingest_input": ("https://example.com",),
    "analyze": ([{"id": "n1"}], []),
    "query_graph": (RESULT, "n1"),
    "query_documents": (RESULT,),
    "query_repository": (RESULT,),
    "query_knowledge": (RESULT,),
    "query_repo": (RESULT,),
    "query_semantics": (RESULT,),
    "compile_document": ("hello world",),
    "compile_repository": ("src",),
    "validate_replay_equivalence": (ENVELOPE, dict(ENVELOPE)),
    "reconstruct_runtime": ({"unified_runtime_graph": GRAPH},),
    "version": None,  # value, not callable
}

GENERIC_CANDIDATES = [
    (GRAPH,),
    (RESULT,),
    ([{"id": "n1"}],),
    ({"a": 1},),
    ("https://example.com",),
    ([],),
    ({},),
    (),
]


def canon(v):
    try:
        return json.dumps(v, sort_keys=True, default=str)
    except Exception:
        return repr(v)


def try_call(fn, args):
    out = fn(*args)
    return out


def main() -> int:
    names = sorted(getattr(w, "__all__", []))
    rows = []
    executed = deterministic = 0
    for n in names:
        obj = getattr(w, n)
        rec = {"name": n, "importable": True, "callable": callable(obj),
               "executed": False, "deterministic": None, "via": None}
        if not callable(obj):
            rec["executed"] = True  # a value (version) is trivially "usable"
            rec["via"] = "value"
            executed += 1
            rows.append(rec)
            continue
        attempts = []
        if n in CURATED and CURATED[n] is not None:
            attempts.append(("curated", CURATED[n]))
        attempts += [("generic", c) for c in GENERIC_CANDIDATES]
        for via, args in attempts:
            try:
                r1 = try_call(obj, args)
                rec["executed"] = True
                rec["via"] = via
                executed += 1
                try:
                    r2 = try_call(obj, args)
                    rec["deterministic"] = canon(r1) == canon(r2)
                    if rec["deterministic"]:
                        deterministic += 1
                except Exception:
                    rec["deterministic"] = None
                break
            except Exception:
                continue
        rows.append(rec)
    out = {
        "measured_at": datetime.now(timezone.utc).isoformat(),
        "language": "python",
        "total": len(names),
        "importable": len(names),
        "callable": sum(1 for r in rows if r["callable"]),
        "executed": executed,
        "deterministic_of_executed": deterministic,
        "symbols": rows,
    }
    p = r"C:\Projects\WebWeaveX\docs\specs\python_execution.json"
    open(p, "w", encoding="utf-8").write(json.dumps(out, indent=2))
    print(f"python execution: {executed}/{len(names)} executed, {deterministic} deterministic")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
