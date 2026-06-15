#!/usr/bin/env python3
"""Session-3 cross-language golden vectors from canonical Python 2.1.0.

Run from a materialized Python-branch checkout:

    python tools/gen_java_parity_vectors_s3.py <out.json>

Covers query / memory / reconstruction. Each entry stores the inputs plus the
canonical `stable_serialize` of the Python output and its `compute_kaalka_hash`.
The Java test reconstructs inputs, recomputes, and asserts byte-equality.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.query.graph_query_engine import query_graph
from core.query.ontology_query_engine import query_knowledge
from core.runtime_graph.runtime_graph_query_engine import query_runtime_graph
from core.graph.topology_reasoning_engine import reason_topology
from core.memory.runtime_memory_engine import build_runtime_memory
from core.memory.runtime_query_engine import query_runtime_memory
from core.memory.runtime_search_engine import search_runtime_memory
from core.reconstruction.runtime_reconstruction_engine import reconstruct_runtime
from core.reconstruction.runtime_memory_reconstruction import reconstruct_runtime_memory
from core.graph.graph_reconstruction_engine import reconstruct_graph
from core.reconstruction.browser_reconstruction_engine import reconstruct_browser_runtime
from core.reconstruction.runtime_validation_engine import validate_reconstructed_runtime


def entry(name, inputs, value):
    return {
        "name": name,
        "inputs": inputs,
        "serialized": stable_serialize(value),
        "hash": compute_kaalka_hash(value),
    }


# Reusable graphs/edges.
G_VALID = {
    "nodes": [{"id": "a"}, {"id": "b"}, {"id": "c"}],
    "edges": [{"from": "a", "to": "b"}, {"from": "b", "to": "c"}, {"from": "a", "to": "c"}],
}
G_TYPED = {"nodes": [{"id": "n1", "type": "x"}, {"id": "n2", "type": "y"}, {"id": "n3", "type": "x"}], "edges": []}
G_DANGLING = {"nodes": [{"id": "a"}], "edges": [{"from": "a", "to": "missing"}, {"type": "bad", "from": "a", "to": "a"}]}
EDGES_KNOW = [
    {"from": "p", "to": "q", "evidence": ["src1"], "contradictions": {"pairs": [["x", "y"]]}},
    {"from": "q", "to": "r", "evidence": ["src2"]},
    {"from": "z", "to": "w"},  # missing evidence -> rejected
]


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 3: query/memory/reconstruction)"}

    g_badedge = {"nodes": [{"id": "a"}, {"id": "b"}],
                 "edges": [{"from": "a"}, {"from": "a", "to": "b", "evidence": "ev"}, {"from": "a", "to": "b"}]}
    out["query_graph"] = [
        entry("qg_valid", {"graph": G_VALID, "node": ""}, query_graph(G_VALID, "")),
        entry("qg_node", {"graph": G_VALID, "node": "a"}, query_graph(G_VALID, "a")),
        entry("qg_dangling", {"graph": G_DANGLING, "node": ""}, query_graph(G_DANGLING, "")),
        entry("qg_badedge", {"graph": g_badedge, "node": "b"}, query_graph(g_badedge, "b")),
    ]

    out["query_runtime_graph"] = [
        entry("qrg_all", {"graph": G_TYPED, "query": {}}, query_runtime_graph(G_TYPED, {})),
        entry("qrg_typed", {"graph": G_TYPED, "query": {"type": "x"}}, query_runtime_graph(G_TYPED, {"type": "x"})),
    ]

    edges_stages = [
        {"from": "p", "to": "q", "evidence": "single", "lineage": {"stages": [{"stage": "prior"}], "depth": 1}},
        {"from": "", "to": "q", "evidence": ["e"]},  # missing endpoint
    ]
    out["query_knowledge"] = [
        entry("qk_basic", {"entities": ["alpha", "beta"], "edges": EDGES_KNOW},
              query_knowledge(["alpha", "beta"], EDGES_KNOW)),
        entry("qk_empty", {"entities": [], "edges": []}, query_knowledge([], [])),
        entry("qk_stages", {"entities": ["", "gamma"], "edges": edges_stages},
              query_knowledge(["", "gamma"], edges_stages)),
    ]

    out["reason_topology"] = [
        entry("rt_valid", {"graph": G_VALID}, reason_topology(G_VALID)),
        entry("rt_hub", {"graph": {"nodes": [{"id": n} for n in "abcd"],
                                   "edges": [{"from": "a", "to": x} for x in "bcd"] + [{"from": "b", "to": "c"}]}},
              reason_topology({"nodes": [{"id": n} for n in "abcd"],
                               "edges": [{"from": "a", "to": x} for x in "bcd"] + [{"from": "b", "to": "c"}]})),
    ]

    history = [
        {"tick": 3, "kind": "workflow", "source": "w"},
        {"tick": 1, "kind": "sync", "source": "s"},
        {"step": 2, "kind": "evolution", "source": "e"},
    ]
    lineage = [{"id": "L2"}, {"id": "L1"}]
    relations = [{"from": "b", "to": "a"}, {"from": "a", "to": "c"}]
    memory = build_runtime_memory(history, lineage, relations)
    out["build_runtime_memory"] = [
        entry("brm_basic", {"runtime_history": history, "lineage": lineage, "semantic_relations": relations}, memory),
        entry("brm_empty", {}, build_runtime_memory()),
    ]

    mem_topo = {
        "semantic_relations": [{"from": "a", "to": "b", "weight": 3, "ok": True, "note": None}],
        "lineage": [{"id": "x"}],
        "runtime_history": [{"runtime": "browser", "tick": 1}, {"runtime": "node", "tick": 2}],
        "synchronization_history": [{"kind": "sync"}],
    }
    out["query_runtime_memory"] = [
        entry("qrm_semantic", {"memory": memory, "query_type": "semantic", "term": "a"},
              query_runtime_memory(memory, "semantic", "a")),
        entry("qrm_lineage", {"memory": memory, "query_type": "lineage", "term": "L"},
              query_runtime_memory(memory, "lineage", "L")),
        entry("qrm_sync", {"memory": memory, "query_type": "sync", "term": ""},
              query_runtime_memory(memory, "sync", "")),
        entry("qrm_topology", {"memory": mem_topo, "query_type": "topology", "term": "browser"},
              query_runtime_memory(mem_topo, "topology", "browser")),
        entry("qrm_else", {"memory": mem_topo, "query_type": "other", "term": "browser"},
              query_runtime_memory(mem_topo, "other", "browser")),
        entry("qrm_repr", {"memory": mem_topo, "query_type": "semantic", "term": "a"},
              query_runtime_memory(mem_topo, "semantic", "a")),
    ]

    index = {
        "entity_index": {"Alpha": 1, "Beta": 2},
        "workflow_index": {"WF1": "a"},
        "connector_index": {"Conn": "x"},
        "graph_index": {"G": 9},
    }
    out["search_runtime_memory"] = [
        entry("srm_semantic", {"index": index, "term": "alp", "search_type": "semantic"},
              search_runtime_memory(index, "alp", "semantic")),
        entry("srm_graph", {"index": index, "term": "", "search_type": "graph"},
              search_runtime_memory(index, "", "graph")),
        entry("srm_structural", {"index": index, "term": "a", "search_type": "structural"},
              search_runtime_memory(index, "a", "structural")),
        entry("srm_lineage", {"index": index, "term": "wf", "search_type": "lineage"},
              search_runtime_memory(index, "wf", "lineage")),
    ]

    out["reconstruct_runtime"] = [
        entry("rr_basic", {"semantic_ir": {"s": 1}, "runtime_graph": {"nodes": [{"id": "a"}]}, "runtime_type": "browser", "tick": 2},
              reconstruct_runtime(semantic_ir={"s": 1}, runtime_graph={"nodes": [{"id": "a"}]}, runtime_type="browser", tick=2)),
        entry("rr_empty", {}, reconstruct_runtime()),
    ]

    mem_ir = {"runtime_history": [{"kind": "sync", "x": 1}, {"kind": "workflow"}], "semantic": {"s": 1},
              "lineage": {"lineage": [{"id": "b"}, {"id": "a"}]}, "knowledge": {"k": 1}, "memory_graphs": {"g": 1}}
    mem_ir_wrapped = {"runtime_history": {"runtime_history": [{"kind": "sync", "n": 1}]}}
    out["reconstruct_runtime_memory"] = [
        entry("rrm_basic", {"memory_ir": mem_ir}, reconstruct_runtime_memory(memory_ir=mem_ir)),
        entry("rrm_empty", {}, reconstruct_runtime_memory()),
        entry("rrm_wrapped", {"memory_ir": mem_ir_wrapped, "semantic": {"sem": 1}, "lineage": {"lineage": [{"id": "z"}]}},
              reconstruct_runtime_memory(memory_ir=mem_ir_wrapped, semantic={"sem": 1}, lineage={"lineage": [{"id": "z"}]})),
    ]

    sysg = {"nodes": [{"id": "b"}, "a", {"id": ""}], "edges": [{"from": "a", "to": "b"}, {"type": "x", "from": "a", "to": "b"}],
            "components": [{"name": "c"}], "relationships": [{"from": "b", "to": "c"}]}
    sysg_comp = {"components": [{"name": "svc1"}, {"name": "svc2"}], "relationships": [{"from": "svc1", "to": "svc2"}]}
    out["reconstruct_graph"] = [
        entry("rg_basic", {"system_graph": sysg}, reconstruct_graph(sysg)),
        entry("rg_empty", {"system_graph": {}}, reconstruct_graph({})),
        entry("rg_comp", {"system_graph": sysg_comp}, reconstruct_graph(sysg_comp)),
        entry("rg_none", {"system_graph": None}, reconstruct_graph(None)),
    ]

    rb_rich_kw = {
        "browser_ir": {"routes": {"history": [{"path": "/x"}]}, "navigation": {"history": [{"path": "/n", "order": 1}]}},
        "interaction_ir": {
            "tab_states": {"tabs": [{"path": "/t1"}, {"path": "/t0"}]},
            "route_transitions": {"routes": [{"path": "/r2", "order": 2}, {"path": "/r1", "order": 1}]},
            "interactions": [{"i": 1}, {"i": 2}],
        },
        "session": {"session_storage": {"s": 1}, "cookies": [{"name": "z"}]},
        "dom": {"structure": {"root": 1}},
        "streaming": {"stream": True},
    }
    out["reconstruct_browser"] = [
        entry("rb_basic", {
            "browser_ir": {"url": "/home"},
            "interaction_ir": {"interactions": [{"a": 1}]},
            "identity": {"id": "x"},
            "session": {"authenticated": True, "cookies": [{"name": "b"}, {"name": "a"}],
                        "local_storage": {"k": "v"}},
        }, reconstruct_browser_runtime(
            browser_ir={"url": "/home"}, interaction_ir={"interactions": [{"a": 1}]},
            identity={"id": "x"}, session={"authenticated": True, "cookies": [{"name": "b"}, {"name": "a"}],
                                           "local_storage": {"k": "v"}})),
        entry("rb_rich", rb_rich_kw, reconstruct_browser_runtime(**rb_rich_kw)),
        entry("rb_nav", {
            "browser_ir": {"navigation": {"history": [{"path": "/b", "order": 1}, {"path": "/a", "order": 0}]}},
            "dom": {"nodes": {"root": "n"}},
        }, reconstruct_browser_runtime(
            browser_ir={"navigation": {"history": [{"path": "/b", "order": 1}, {"path": "/a", "order": 0}]}},
            dom={"nodes": {"root": "n"}})),
        entry("rb_empty", {}, reconstruct_browser_runtime()),
    ]

    out["validate_reconstructed_runtime"] = [
        entry("vrr_valid", {"runtime": {"reconstructed": True}, "replay": {"replayed": {"x": 1}}},
              validate_reconstructed_runtime(runtime={"reconstructed": True}, replay={"replayed": {"x": 1}})),
        entry("vrr_invalid", {"runtime": {}, "replay": {}},
              validate_reconstructed_runtime(runtime={}, replay={})),
        entry("vrr_topology", {
            "runtime": {"fabricated": True, "replay_safe": True},
            "replay": {"replay_chains": [1]},
            "topology": {"runtime_graph": {"n": 1}, "synchronization_topology": {"s": 1}},
            "execution": {"actions": [{"a": 1}]},
        }, validate_reconstructed_runtime(
            runtime={"fabricated": True, "replay_safe": True},
            replay={"replay_chains": [1]},
            topology={"runtime_graph": {"n": 1}, "synchronization_topology": {"s": 1}},
            execution={"actions": [{"a": 1}]})),
        entry("vrr_notrecon", {"runtime": {"x": 1}, "replay": {"replay_package": {"p": 1}}},
              validate_reconstructed_runtime(runtime={"x": 1}, replay={"replay_package": {"p": 1}})),
        entry("vrr_mut_dict", {
            "runtime": {"reconstructed": True}, "replay": {"replayed": {"x": 1}},
            "mutations": {"mutations": [{"kind": "add"}, {"target": "n"}]},
        }, validate_reconstructed_runtime(
            runtime={"reconstructed": True}, replay={"replayed": {"x": 1}},
            mutations={"mutations": [{"kind": "add"}, {"target": "n"}]})),
        entry("vrr_mut_bad", {
            "runtime": {"reconstructed": True}, "replay": {"replayed": {"x": 1}},
            "mutations": [{"nope": 1}],
        }, validate_reconstructed_runtime(
            runtime={"reconstructed": True}, replay={"replayed": {"x": 1}},
            mutations=[{"nope": 1}])),
    ]

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s3.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors {counts}\n")


if __name__ == "__main__":
    main()
