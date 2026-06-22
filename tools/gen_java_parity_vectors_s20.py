#!/usr/bin/env python3
"""Session-20 cross-language golden vectors from canonical Python 2.1.0.

    python tools/gen_java_parity_vectors_s20.py <out.json>

Covers the dependency-clean core.memory orchestrator (run_runtime_memory,
run_memory_for_extraction) + its ~14 sub-engines + IR. Python is the oracle.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.memory.runtime_memory_orchestrator import run_runtime_memory, run_memory_for_extraction
from core.memory.runtime_history_engine import append_runtime_history
from core.memory.knowledge_memory_engine import build_knowledge_memory
from core.memory.semantic_memory_engine import build_semantic_memory
from core.memory.runtime_lineage_memory_engine import build_runtime_lineage_memory
from core.memory.runtime_graph_memory_engine import build_runtime_memory_graph
from core.memory.runtime_index_engine import build_runtime_index
from core.memory.runtime_replication_engine import replicate_runtime_memory
from core.memory.runtime_convergence_memory_engine import converge_runtime_memory
from core.memory.distributed_memory_engine import build_distributed_memory
from core.memory.runtime_federation_engine import federate_runtime_memory
from core.memory.runtime_merge_engine import merge_runtime_memories
from core.memory.runtime_memory_policy_engine import build_runtime_memory_policy, enforce_memory_policy
from core.memory.runtime_diff_memory_engine import diff_runtime_memory
from core.memory.runtime_snapshot_memory_engine import capture_memory_snapshot
from core.memory.runtime_memory_engine import build_runtime_memory
from core.ir.runtime_memory_ir import compile_runtime_memory_ir, runtime_memory_ir_to_graph

SEM = {"semantic": {"entities": {"entities": [{"id": "e2", "label": "User"}, {"id": "e1", "type": "Order"}],
                                 "relations": [{"from": "e1", "to": "e2", "relation": "owns"}]},
                    "domain": {"domain": "saas"}}}
SOURCES = {
    "semantic": SEM,
    "workflow": {"objective": "extract_dashboard"},
    "sync": {"lineage": [{"id": "s1"}], "drift": {}},
    "evolution": {"selector": {"selectors": [{"original": "#a"}]}, "lineage": [{"id": "ev1"}]},
    "live": {"streams": {"streams": [{"stream_type": "kafka"}]}},
    "extraction": {"x": 1},
    "graph": {"nodes": [{"id": "g1"}], "edges": []},
    "distributed": {"workers": [{"worker_id": "w1"}]},
    "application": {"app": 1},
}
NODES = [{"node_id": "n2", "synced": True}, {"node_id": "n1", "synced": True, "conflicts_resolved": 2}]


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 20: memory orchestrator)"}

    def rrm(name, **kw):
        return ev(name, kw, run_runtime_memory(**kw))
    out["run_runtime_memory"] = [
        rrm("empty"),
        rrm("full", sources=SOURCES, nodes=NODES, tick=2),
        rrm("stored", sources=SOURCES, tick=1,
            stored={"runtime": {"memory_id": "prev", "runtime_history": [{"tick": 0, "kind": "x"}],
                                "lineage": [{"id": "old1"}]}}),
    ]

    def rfe(name, **kw):
        return ev(name, kw, run_memory_for_extraction(**kw))
    out["run_memory_for_extraction"] = [
        rfe("disabled", federated_memory=False),
        rfe("default", sources=SOURCES, nodes=NODES),
        rfe("no_merge", sources=SOURCES, merge_graph=False),
    ]

    # ---- engine-level parity ----
    out["append_runtime_history"] = [
        ev("append", {"history": [{"tick": 2}], "entry": {"tick": 1, "kind": "x"}},
           {"history": append_runtime_history([{"tick": 2}], {"tick": 1, "kind": "x"})}),
    ]
    ENT = [{"id": "e2", "label": "B"}, {"id": "e1", "label": "A"}]
    REL = [{"from": "e1", "to": "e2", "relation": "owns"}]
    out["build_knowledge_memory"] = [
        ev("knowledge", {"entities": ENT, "relations": REL, "topology": {"graphs": [{"g": 1}], "distributed": {"d": 1}}},
           build_knowledge_memory(ENT, REL, {"graphs": [{"g": 1}], "distributed": {"d": 1}})),
    ]
    out["build_semantic_memory"] = [
        ev("sem_empty", {"semantic": {}, "history": []}, build_semantic_memory({}, [])),
        ev("sem_full", {"semantic": SEM, "history": [{"kind": "workflow", "objective": "x"}]},
           build_semantic_memory(SEM, [{"kind": "workflow", "objective": "x"}])),
    ]
    out["build_runtime_lineage_memory"] = [
        ev("lineage", {"selector": [{"original": "#a"}], "workflow": [{"id": "wf:0"}], "sync": [{"id": "s1"}],
                       "evolution": [{"id": "ev1"}], "extraction": [{"id": "ex1"}]},
           build_runtime_lineage_memory([{"original": "#a"}], [{"id": "wf:0"}], [{"id": "s1"}],
                                        [{"id": "ev1"}], [{"id": "ex1"}])),
    ]
    out["build_runtime_memory_graph"] = [
        ev("graph", {"entities": ENT, "relations": REL}, build_runtime_memory_graph(ENT, REL)),
        ev("graph_empty", {"entities": [], "relations": []}, build_runtime_memory_graph([], [])),
    ]
    out["build_runtime_index"] = [
        ev("index", {"entities": ENT, "workflows": [{"id": "w1"}], "graphs": [{"g": 1}],
                     "streams": [{"s": 1}], "connectors": [{"c": 1}]},
           build_runtime_index(ENT, [{"id": "w1"}], [{"g": 1}], [{"s": 1}], [{"c": 1}])),
    ]
    RT = build_runtime_memory(runtime_history=[{"tick": 1, "kind": "sync"}], lineage=[{"id": "l1"}],
                              semantic_relations=REL)
    out["replicate_runtime_memory"] = [
        ev("replicate", {"source": RT, "nodes": NODES}, replicate_runtime_memory(RT, NODES)),
    ]
    REPL = replicate_runtime_memory(RT, NODES)
    out["converge_runtime_memory"] = [
        ev("converge", {"replicas": REPL["replicas"]}, converge_runtime_memory(REPL["replicas"])),
        ev("converge_empty", {"replicas": []}, converge_runtime_memory([])),
    ]
    out["build_distributed_memory"] = [
        ev("distributed", {"nodes": NODES}, build_distributed_memory(NODES)),
    ]
    out["federate_runtime_memory"] = [
        ev("federate", {"memories": [RT, {"runtime_history": [{"tick": 0}], "lineage": [{"id": "x"}]}]},
           federate_runtime_memory([RT, {"runtime_history": [{"tick": 0}], "lineage": [{"id": "x"}]}])),
    ]
    out["merge_runtime_memories"] = [
        ev("merge", {"memories": [dict(RT), {"memory_id": "z", "runtime_history": [{"tick": 0, "kind": "a"}]}]},
           merge_runtime_memories([dict(RT), {"memory_id": "z", "runtime_history": [{"tick": 0, "kind": "a"}]}])),
    ]
    POL = build_runtime_memory_policy()
    out["build_runtime_memory_policy"] = [ev("policy", {}, POL)]
    out["enforce_memory_policy"] = [
        ev("enforce", {"policy": POL, "history": [{"t": 1}], "lineage": [{"id": "l"}], "replicas": 2},
           enforce_memory_policy(POL, [{"t": 1}], [{"id": "l"}], 2)),
    ]
    out["diff_runtime_memory"] = [
        ev("diff", {"previous": {"memory_id": "a", "lineage": [{"id": "l1"}], "runtime_history": []},
                    "current": RT},
           diff_runtime_memory({"memory_id": "a", "lineage": [{"id": "l1"}], "runtime_history": []}, RT)),
    ]
    out["capture_memory_snapshot"] = [
        ev("snapshot", {"state": {"runtime": RT, "graph": {"g": 1}}, "tick": 5},
           capture_memory_snapshot({"runtime": RT, "graph": {"g": 1}}, tick=5)),
    ]
    # ---- extra coverage vectors (conflict branch + comparator tie tiers) ----
    out["converge_runtime_memory"].append(
        ev("converge_conflict", {"replicas": [{"memory_id": "a"}, {"memory_id": "b"}]},
           converge_runtime_memory([{"memory_id": "a"}, {"memory_id": "b"}])))
    REL_TIES = [{"from": "a", "to": "b", "relation": "z"}, {"from": "a", "to": "b", "relation": "a"},
                {"from": "a", "to": "c", "relation": "x"}]
    ENT_TIES = [{"id": "e1", "label": "A"}, {"id": "e1", "label": "B"}, {"id": "e0"}]
    out["build_knowledge_memory"].append(
        ev("knowledge_ties", {"entities": ENT_TIES, "relations": REL_TIES, "topology": {}},
           build_knowledge_memory(ENT_TIES, REL_TIES, {})))
    out["build_runtime_memory_graph"].append(
        ev("graph_ties", {"entities": ENT_TIES, "relations": REL_TIES},
           build_runtime_memory_graph(ENT_TIES, REL_TIES)))
    FED_MEMS = [{"runtime_history": [{"tick": 1}, {"tick": 1}], "lineage": [{"id": "b"}, {"id": "a"}],
                "semantic_relations": [{"from": "a", "to": "b"}, {"from": "a", "to": "a"}]},
               {"runtime_history": [{"tick": 0}], "lineage": [{"id": "c"}], "semantic_relations": []}]
    out["federate_runtime_memory"].append(
        ev("federate_ties", {"memories": FED_MEMS}, federate_runtime_memory(FED_MEMS)))
    MRG = [{"memory_id": "b", "runtime_history": [{"tick": 1, "kind": "b", "source": "y"},
                                                  {"tick": 1, "kind": "b", "source": "x"},
                                                  {"tick": 1, "kind": "a", "source": "z"}]},
           {"memory_id": "a", "runtime_history": [{"tick": 0}]}]
    out["merge_runtime_memories"].append(
        ev("merge_ties", {"memories": [dict(x) for x in MRG]},
           merge_runtime_memories([dict(x) for x in MRG])))
    out["build_runtime_lineage_memory"].append(
        ev("lineage_ties", {"selector": [{"id": "z"}, {"id": "a"}], "workflow": [], "sync": [],
                            "evolution": [], "extraction": []},
           build_runtime_lineage_memory([{"id": "z"}, {"id": "a"}], [], [], [], [])))
    out["build_runtime_index"].append(
        ev("index_no_id", {"entities": [{"x": 1}, {"label": "L"}], "workflows": [{"objective": "o"}],
                           "graphs": [], "streams": [], "connectors": []},
           build_runtime_index([{"x": 1}, {"label": "L"}], [{"objective": "o"}], [], [], [])))

    PAYLOAD = run_runtime_memory(sources=SOURCES, nodes=NODES, tick=1)
    IR = compile_runtime_memory_ir(PAYLOAD)
    out["compile_runtime_memory_ir"] = [ev("ir", {"payload": PAYLOAD}, IR)]
    out["runtime_memory_ir_to_graph"] = [
        ev("ir2graph", {"ir": IR}, runtime_memory_ir_to_graph(IR)),
        ev("ir2graph_empty", {"ir": {}}, runtime_memory_ir_to_graph({})),
    ]

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s20.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors across {len(counts)} sections\n")


if __name__ == "__main__":
    main()
