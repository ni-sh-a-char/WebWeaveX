#!/usr/bin/env python3
"""Session-2 cross-language golden vectors from canonical Python 2.1.0.

Run from a materialized Python-branch checkout (so `core` is importable):

    python tools/gen_java_parity_vectors_s2.py <out.json>

Covers kernel / graph / ir / persistence / fingerprint / replay. Each entry
stores the inputs plus the canonical `stable_serialize` of the Python output and
its `compute_kaalka_hash`; string-returning functions also store the exact
string. The Java test reconstructs inputs, recomputes outputs, and asserts
byte-equality.
"""
from __future__ import annotations

import json
import sys

from core.contracts.graph_contracts import RuntimeGraphContract
from core.contracts.runtime_contracts import UniversalInput
from core.crypto.kaalka_engine import hex_fingerprint
from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.global_runtime_fingerprint import compute_global_runtime_fingerprint
from core.determinism.runtime_graph_parity import (
    build_parity_runtime_graph,
    normalize_runtime_graph,
)
from core.ir.multimodal_ir import compile_multimodal_ir
from core.ir.unified_runtime_ir import (
    compile_unified_runtime_ir,
    unified_runtime_ir_to_graph,
)
from core.replay.replay_equivalence_engine import validate_replay_equivalence
from core.determinism.normalization import stable_serialize


def out_dict(name, inputs, value):
    return {
        "name": name,
        "inputs": inputs,
        "serialized": stable_serialize(value),
        "hash": compute_kaalka_hash(value),
    }


def out_str(name, inputs, value):
    return {"name": name, "inputs": inputs, "string": value}


def main() -> None:
    universal_input = []
    UI_CASES = [
        ("ui_minimal", {"source": "doc.txt"}),
        ("ui_full", {
            "source": "s", "source_type": "web", "url": "https://x", "path": "/p",
            "session": {"k": "v"}, "options": {"z": 1, "a": 2}, "tick": 7,
        }),
        ("ui_options_sort", {"source": "x", "options": {"c": 3, "a": 1, "b": 2}}),
    ]
    for name, kw in UI_CASES:
        universal_input.append(out_dict(name, kw, UniversalInput(**kw).to_dict()))

    graph = []
    GRAPH_SOURCES = [
        ("g_single", {"text": {"source": "hello"}}),
        ("g_multi", {"web": {"u": 1}, "doc": {"p": 2}, "api": {"a": 3}}),
        ("g_unicode", {"é": {"v": 1}, "a": {"v": 2}, "😀": {"v": 3}}),
    ]
    for name, sources in GRAPH_SOURCES:
        g = build_parity_runtime_graph(sources)
        graph.append({
            "name": name,
            "inputs": sources,
            "built_serialized": stable_serialize(g),
            "built_hash": compute_kaalka_hash(g),
            "fingerprint": compute_kaalka_hash(normalize_runtime_graph(g)),
        })

    graph_contract = []
    CONTRACT_CASES = [
        ("gc_mixed", {
            "nodes": [{"id": "b", "type": "t"}, {"id": "a", "type": "t"}],
            "edges": [{"from": "b", "to": "a", "type": "e"}, {"source": "a", "target": "b"}],
        }),
        ("gc_empty", {}),
    ]
    for name, g in CONTRACT_CASES:
        graph_contract.append(out_dict(name, g, RuntimeGraphContract.normalize(g)))

    unified_ir = []
    UIR_CASES = [
        ("uir_empty", {}),
        ("uir_phases", {
            "registry": {"phases": {"semantic": {"s": 1}, "memory": {"m": 2}}},
            "graph": {"nodes": [{"id": "n1"}], "edges": [], "bounded": True},
            "bus": [{"tick": 2, "order": 1, "e": "b"}, {"tick": 1, "order": 5, "e": "a"}],
            "phase_results": [{"phase": "z"}, {"phase": "a"}],
            "sources": {"browser": {"b": 1}},
        }),
    ]
    for name, kw in UIR_CASES:
        ir = compile_unified_runtime_ir(**kw)
        entry = out_dict(name, kw, ir)
        entry["to_graph_serialized"] = stable_serialize(unified_runtime_ir_to_graph(ir))
        entry["to_graph_hash"] = compute_kaalka_hash(unified_runtime_ir_to_graph(ir))
        unified_ir.append(entry)

    multimodal_ir = []
    MM_CASES = [
        ("mm_basic", {
            "layout": {"blocks": [{"t": "h1"}], "x": 1}, "tables": {"t": []},
            "forms": {"f": 1}, "charts": {"c": 2}, "ui": {"u": 3},
        }),
        ("mm_noblocks", {"layout": {"y": 9}, "tables": {}, "forms": {}, "charts": {}, "ui": {}}),
    ]
    for name, kw in MM_CASES:
        multimodal_ir.append(out_dict(name, kw, compile_multimodal_ir(**kw)))

    fingerprint = []
    FP_CASES = [
        ("fp_str", "hello world", "webweavex"),
        ("fp_str_token", "payload", "tok"),
        ("fp_unicode", "café 🚀", "webweavex"),
        ("fp_dict", {"b": 1, "a": 2.0, "n": None}, "webweavex"),
        ("fp_list", [3, 1, 2, "x"], "t2"),
        ("fp_number", 12345, "webweavex"),
    ]
    for name, payload, token in FP_CASES:
        fingerprint.append(out_str(name, {"payload": payload, "token": token},
                                   hex_fingerprint(payload, token)))

    global_fp = []
    GFP_CASES = [
        ("gfp_basic", {
            "extraction": {"pipeline_hash": "ph1", "runtime": {}, "browser_ir": {"runtime_identity": "id1"}},
            "graph": {"nodes": [{"id": "n2"}, {"id": "n1"}], "edges": [{"source": "n1", "target": "n2", "type": "e"}]},
        }),
        ("gfp_memory", {
            "extraction": {"pipeline_hash": "p", "unified_runtime_graph": {"nodes": [{"id": "a"}], "edges": []}},
            "memory": {"stable_hash": "mh", "memory": {"runtime_history": [1, 2, 3]}},
            "sync": {"convergence": {"converged": True}},
            "reconstruction": {"runtime": {"runtime_id": "rid"}},
            "kaalka_seal": "seal1",
        }),
        ("gfp_dom", {
            "extraction": {
                "runtime": {"dom_stabilization": {"stabilized_hash": "domh"}},
                "browser_ir": {"runtime_identity": "bid"}, "pipeline_hash": "p",
            },
            "graph": {"nodes": [{"id": "a"}], "edges": [{"from": "a", "to": "b"}]},
        }),
        ("gfp_spa", {
            "extraction": {"runtime": {"spa_stabilization": {"stable_dom_hash": "spah"}}},
            "graph": {},
        }),
    ]
    for name, kw in GFP_CASES:
        global_fp.append(out_str(name, kw, compute_global_runtime_fingerprint(**kw)))

    replay = []
    g1 = {"nodes": [{"id": "n1"}, {"id": "n2"}], "edges": [{"source": "n1", "target": "n2", "type": "e"}]}
    g1_shuffled = {"nodes": [{"id": "n2"}, {"id": "n1"}], "edges": [{"source": "n1", "target": "n2", "type": "e"}]}
    g2 = {"nodes": [{"id": "x"}], "edges": []}
    REPLAY_CASES = [
        ("replay_equivalent", {
            "original": {"unified_runtime_graph": g1, "pipeline_hash": "p", "browser_ir": {"runtime_identity": "i"}},
            "replayed": {"unified_runtime_graph": g1_shuffled, "pipeline_hash": "p", "browser_ir": {"runtime_identity": "i"}},
        }),
        ("replay_divergent", {
            "original": {"unified_runtime_graph": g1, "pipeline_hash": "p"},
            "replayed": {"unified_runtime_graph": g2, "pipeline_hash": "p"},
        }),
    ]
    for name, kw in REPLAY_CASES:
        replay.append(out_dict(name, kw, validate_replay_equivalence(**kw)))

    result = {
        "source": "Python 2.1.0 canonical (session 2: kernel/graph/ir/persistence/fingerprint/replay)",
        "universal_input": universal_input,
        "graph": graph,
        "graph_contract": graph_contract,
        "unified_ir": unified_ir,
        "multimodal_ir": multimodal_ir,
        "fingerprint": fingerprint,
        "global_fingerprint": global_fp,
        "replay": replay,
    }
    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s2.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in result.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {counts}\n")


if __name__ == "__main__":
    main()
