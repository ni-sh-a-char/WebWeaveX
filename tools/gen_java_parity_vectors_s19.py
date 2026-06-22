#!/usr/bin/env python3
"""Session-19 cross-language golden vectors from canonical Python 2.1.0.

    python tools/gen_java_parity_vectors_s19.py <out.json>

Covers the dependency-clean remainder slice: save/load_distributed_checkpoint,
save/load_native_runtime, replay_semantic_runtime, execute_runtime_objective, query_repository,
authenticate_runtime (page=None path). Python is the oracle.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.distributed_extraction.distributed_checkpoint_engine import (
    save_distributed_checkpoint, load_distributed_checkpoint)
from core.native.native_memory_engine import save_native_runtime, load_native_runtime
from core.semantic.semantic_replay_engine import replay_semantic_runtime
from core.application.objective_execution_engine import execute_runtime_objective
from core.agents.repository_query_engine import query_repository
from core.auth.authentication_runtime_engine import authenticate_runtime

KEY = "s19-key-2024"


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 19: clean remainder slice)"}

    # replay_semantic_runtime
    out["replay_semantic_runtime"] = [
        ev("empty", {"memory": {}}, replay_semantic_runtime({})),
        ev("null", {}, replay_semantic_runtime({})),  # absent "memory" -> Java null guard
        ev("full", {"memory": {"semantic_graph": {"g": 1}, "ontology": {"o": 1},
                               "semantic_workflows": {"w": 1}, "runtime_semantics": {"r": 1},
                               "entity_mappings": {"e": 1}}},
           replay_semantic_runtime({"semantic_graph": {"g": 1}, "ontology": {"o": 1},
                                    "semantic_workflows": {"w": 1}, "runtime_semantics": {"r": 1},
                                    "entity_mappings": {"e": 1}})),
    ]

    # execute_runtime_objective
    WG = {"nodes": [{"id": "n1"}, {"id": "n2"}]}
    AG = {"nodes": [{"id": "a1"}]}
    NAV = {"routes": [{"path": "/home"}]}
    out["execute_runtime_objective"] = [
        ev("login", {"objective": "login", "workflow_graph": WG, "action_graph": AG, "navigation": NAV,
                     "adaptive_runtime": {"x": 1}},
           execute_runtime_objective("login", WG, AG, NAV, {"x": 1})),
        ev("unknown", {"objective": "custom", "workflow_graph": {}, "action_graph": {}, "navigation": {},
                       "adaptive_runtime": None},
           execute_runtime_objective("custom", {}, {}, {}, None)),
        ev("dashboard", {"objective": "extract_dashboard", "workflow_graph": WG, "action_graph": AG,
                         "navigation": {"routes": [{"path": "/d"}, {"path": "/x"}]}, "adaptive_runtime": {}},
           execute_runtime_objective("extract_dashboard", WG, AG, {"routes": [{"path": "/d"}, {"path": "/x"}]}, {})),
        ev("null_graphs", {"objective": "login"}, execute_runtime_objective("login", {}, {}, {}, None)),
        ev("export", {"objective": "export_report", "workflow_graph": WG, "action_graph": AG,
                      "navigation": NAV, "adaptive_runtime": {"a": 1}},
           execute_runtime_objective("export_report", WG, AG, NAV, {"a": 1})),
    ]

    # query_repository
    RESULT = {"content": {"repository": {"files": ["a.py"], "name": "repo1", "tree": {"x": 1}}}}
    out["query_repository"] = [
        ev("no_key", {"result": RESULT, "key": ""}, {"repo": query_repository(RESULT, "")}),
        ev("with_key", {"result": RESULT, "key": "name"}, {"repo": query_repository(RESULT, "name")}),
        ev("missing_key", {"result": RESULT, "key": "absent"}, {"repo": query_repository(RESULT, "absent")}),
        ev("empty_result", {"result": {}, "key": ""}, {"repo": query_repository({}, "")}),
        ev("null_result", {"key": ""}, {"repo": query_repository({}, "")}),
        ev("content_no_repo", {"result": {"content": {"x": 1}}, "key": ""},
           {"repo": query_repository({"content": {"x": 1}}, "")}),
    ]

    # authenticate_runtime (page=None -> missing_page, method varies)
    out["authenticate_runtime"] = [
        ev("default", {"credentials": {}, "config": {}}, authenticate_runtime(None, {}, {})),
        ev("form", {"credentials": {"username": "u"}, "config": {"method": "form_login"}},
           authenticate_runtime(None, {"username": "u"}, {"method": "form_login"})),
        ev("token", {"credentials": {"tokens": [1]}, "config": {"method": "  token_injection  "}},
           authenticate_runtime(None, {"tokens": [1]}, {"method": "  token_injection  "})),
        ev("null_config", {"credentials": {}}, authenticate_runtime(None, {}, {})),
    ]

    # save/load_distributed_checkpoint + save/load_native_runtime (real FS)
    d = tempfile.mkdtemp(prefix="wwx_s19_")
    persistence = [
        ("distributed_checkpoint", save_distributed_checkpoint, load_distributed_checkpoint, "checkpoint",
         [("simple", {"queue": [{"t": 1}], "tick": 3, "bounded": True}),
          ("unicode", {"note": "café \U0001F600", "用户": 1, "bounded": True}),
          ("empty", {})]),
        ("native_runtime", save_native_runtime, load_native_runtime, "runtime",
         [("simple", {"windows": {"w1": {}}, "bounded": True}),
          ("unicode", {"note": "café \U0001F600", "bounded": True}),
          ("empty", {})]),
    ]
    for engine, save_fn, load_fn, field, cases in persistence:
        save_vecs, load_vecs = [], []
        for nm, mem in cases:
            fname = f"{engine}_{nm}.json"
            p = os.path.join(d, fname)
            save_fn(p, mem, KEY)
            with open(p, encoding="utf-8") as fh:
                content = fh.read()
            save_vecs.append({"name": nm, "inputs": {"filename": fname, "payload": mem, "key": KEY},
                              "file_content": content})
            load_ret = load_fn(p, KEY)
            load_vecs.append({"name": "load_" + nm, "file_content": content, "key": KEY,
                              "serialized": stable_serialize(load_ret), "hash": compute_kaalka_hash(load_ret)})
        miss = load_fn(os.path.join(d, f"{engine}_nope.json"), KEY)
        load_vecs.append({"name": "load_missing", "missing": True, "key": KEY,
                          "serialized": stable_serialize(miss), "hash": compute_kaalka_hash(miss)})
        out[f"save_{engine}"] = save_vecs
        out[f"load_{engine}"] = load_vecs

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s19.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors across {len(counts)} sections\n")


if __name__ == "__main__":
    main()
