#!/usr/bin/env python3
"""
Canonical runtime probes — executed against materialized origin/python core/.
Outputs are the source of truth for validation/vectors/*.
"""
from __future__ import annotations

import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
STAGING = Path(__file__).resolve().parent / ".py_staging"
VECTORS = ROOT / "validation" / "vectors"

if str(STAGING) not in sys.path:
    sys.path.insert(0, str(STAGING))


def _fp(value: Any) -> str:
    from core.crypto.kaalka_hash_engine import compute_kaalka_hash_payload

    return compute_kaalka_hash_payload(value)


def _graph_hash(graph: dict[str, Any]) -> str:
    from core.contracts.graph_contracts import RuntimeGraphContract
    from core.crypto.kaalka_hash_engine import compute_kaalka_hash

    normalized = RuntimeGraphContract.normalize(graph)
    return compute_kaalka_hash(
        json.dumps(
            {"nodes": normalized.get("nodes", []), "edges": normalized.get("edges", [])},
            sort_keys=True,
            default=str,
        )
    )


def _vector(
    vid: str,
    inp: dict[str, Any],
    out: dict[str, Any],
    *,
    graph: dict[str, Any] | None = None,
    memory: dict[str, Any] | None = None,
    replay: dict[str, Any] | None = None,
    vm: dict[str, Any] | None = None,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "id": vid,
        "input": inp,
        "canonical_output": out,
        "runtime_hash": _fp(out),
        "deterministic_fingerprint": _fp({"input": inp, "output": out}),
    }
    if graph is not None:
        row["graph_hash"] = _graph_hash(graph)
    if memory is not None:
        from core.memory.stable_memory_hash import stable_memory_hash

        row["memory_hash"] = stable_memory_hash(memory)
    if replay is not None:
        row["replay_hash"] = _fp(replay)
    if vm is not None:
        row["vm_hash"] = _fp(vm)
    return row


def probe_graph_vectors() -> list[dict[str, Any]]:
    from core.determinism.runtime_graph_parity import build_parity_runtime_graph

    vectors: list[dict[str, Any]] = []
    for vid, sources in [
        ("graph-session", {"session": {"ok": True}}),
        ("graph-multi", {"session": {"ok": True}, "browser": {"url": "https://example.com"}}),
        ("graph-step", {"step": "login", "tick": 1}),
    ]:
        graph = build_parity_runtime_graph(sources)
        vectors.append(_vector(vid, {"sources": sources}, graph, graph=graph))
    return vectors


def probe_runtime_vectors() -> list[dict[str, Any]]:
    from core.determinism.runtime_graph_parity import build_parity_runtime_graph
    from core.memory.runtime_memory_engine import build_runtime_memory
    from core.reconstruction.runtime_reconstruction_engine import reconstruct_runtime
    from core.crypto.kaalka_runtime_engine import decrypt_value, encrypt_value

    graph = build_parity_runtime_graph({"session": {"ok": True}})
    memory = build_runtime_memory(runtime_history=[{"step": "login", "tick": 1, "kind": "workflow"}])
    rebuilt = reconstruct_runtime(runtime_graph=graph)
    enc = encrypt_value({"agent": "continuity"}, "agent-key")
    dec = json.loads(decrypt_value(enc["encrypted"], "agent-key")["decrypted"])

    return [
        _vector("runtime-memory", {"history": [{"step": "login", "tick": 1, "kind": "workflow"}]}, memory, memory=memory),
        _vector(
            "runtime-reconstruct",
            {"runtime_graph": graph},
            rebuilt,
            graph=graph,
        ),
        _vector(
            "runtime-crypto",
            {"plaintext": {"agent": "continuity"}, "key": "agent-key"},
            {"encrypted": enc["encrypted"], "decrypted": dec, "agent": dec.get("agent")},
        ),
    ]


def probe_replay_vectors() -> list[dict[str, Any]]:
    from core.determinism.runtime_graph_parity import build_parity_runtime_graph
    from core.replay.replay_equivalence_engine import validate_replay_equivalence

    graph = build_parity_runtime_graph({"step": "login"})
    envelope = {
        "bounded": True,
        "unified_runtime_graph": graph,
        "browser_ir": {"runtime_identity": "replay-probe"},
    }
    clone = copy.deepcopy(envelope)
    replay = validate_replay_equivalence(envelope, clone)
    return [_vector("replay-envelope", {"envelope": envelope}, replay, graph=graph, replay=replay)]


def probe_vm_vectors() -> list[dict[str, Any]]:
    from core.bytecode import SemanticInstruction
    from core.vm.semantic_vm_engine import SemanticVirtualMachine

    vm = SemanticVirtualMachine()
    instructions = [
        SemanticInstruction(opcode="LINK", operand={"from": "a", "to": "b"}),
        SemanticInstruction(opcode="NOP", operand={}),
    ]
    out = vm.execute(instructions)
    return [_vector("vm-semantic-link", {"instructions": [{"opcode": "LINK", "operand": {"from": "a", "to": "b"}}, {"opcode": "NOP", "operand": {}}]}, out, vm=out)]


def probe_semantic_vectors() -> list[dict[str, Any]]:
    from core.semantic.ontology_engine import build_semantic_ontology

    entities = [{"type": "Person"}, {"type": "Organization"}, {"type": "Person"}]
    ont = build_semantic_ontology(entities, "operations")
    return [_vector("semantic-ontology", {"entities": entities, "domain": "operations"}, ont)]


def probe_distributed_vectors() -> list[dict[str, Any]]:
    from core.distributed_extraction.distributed_extraction_orchestrator import run_distributed_extraction

    out = run_distributed_extraction(
        [{"task_id": "t1", "url": "https://example.com", "priority": 2}],
        None,
        {},
        0,
        [],
    )
    return [_vector("distributed-extraction", {"tasks": [{"task_id": "t1", "url": "https://example.com", "priority": 2}]}, out)]


def probe_workflow_vectors() -> list[dict[str, Any]]:
    from core.workflows.workflow_execution_engine import execute_workflow_plan

    plan = {
        "objective": "probe",
        "steps": [
            {"id": "s1", "action": "extract", "runtime": "browser"},
            {"id": "s2", "action": "replay", "runtime": "browser"},
        ],
    }
    out = execute_workflow_plan(plan, tick=0)
    return [_vector("workflow-execute", {"plan": plan, "tick": 0}, out)]


def probe_memory_vectors() -> list[dict[str, Any]]:
    from core.memory.runtime_memory_engine import build_runtime_memory

    mem = build_runtime_memory(
        runtime_history=[
            {"step": "login", "tick": 1, "kind": "workflow"},
            {"step": "navigate", "tick": 2, "kind": "workflow"},
        ],
        lineage=[{"id": "L1"}],
    )
    return [_vector("memory-history", {"history": mem["runtime_history"]}, mem, memory=mem)]


def probe_repository_vectors() -> list[dict[str, Any]]:
    # Repository probes use deterministic structure (no live git in CI).
    out = {
        "repository_id": _fp({"kind": "repository", "path": "."}),
        "languages": ["typescript", "python"],
        "bounded": True,
    }
    return [_vector("repository-probe", {"path": "."}, out)]


def probe_browser_vectors() -> list[dict[str, Any]]:
    from core.determinism.runtime_graph_parity import build_parity_runtime_graph

    graph = build_parity_runtime_graph({"browser": {"url": "https://example.com", "dom_hash": "abc"}})
    out = {"graph": graph, "bounded": True}
    return [_vector("browser-graph", {"url": "https://example.com"}, out, graph=graph)]


def probe_continuation_vectors() -> list[dict[str, Any]]:
    from core.crypto.kaalka_runtime_engine import compute_deterministic_hash_payload

    session = {"cookies": [], "headers": {}, "session_id": "sess-probe"}
    out = {
        "session_hash": compute_deterministic_hash_payload(session),
        "continuation": False,
        "bounded": True,
    }
    return [_vector("continuation-session", {"session": session}, out)]


def probe_parser_vectors() -> list[dict[str, Any]]:
    out = {"registry": [], "bounded": True, "parser_count": 0}
    return [_vector("parser-registry", {}, out)]


def probe_reconstruction_vectors() -> list[dict[str, Any]]:
    from core.determinism.runtime_graph_parity import build_parity_runtime_graph
    from core.reconstruction.runtime_reconstruction_engine import reconstruct_runtime

    graph = build_parity_runtime_graph({"session": {"ok": True}, "workflow": {"step": 1}})
    rebuilt = reconstruct_runtime(
        runtime_graph=graph,
        tick=3,
        runtime_type="browser",
        semantic_ir={"entities": []},
        workflow_ir={"objective": "probe"},
    )
    return [
        _vector(
            "reconstruction-full",
            {
                "runtime_graph": graph,
                "tick": 3,
                "runtime_type": "browser",
                "semantic_ir": {"entities": []},
                "workflow_ir": {"objective": "probe"},
            },
            rebuilt,
            graph=graph,
        )
    ]


def probe_ontology_vectors() -> list[dict[str, Any]]:
    from core.semantic.ontology_engine import build_semantic_ontology

    entities = [{"type": "Entity"}, {"type": "Process"}]
    ont = build_semantic_ontology(entities, "operations")
    return [_vector("ontology-classes", {"entities": entities, "domain": "operations"}, ont)]


def probe_continuation_memory_vectors() -> list[dict[str, Any]]:
    from core.memory.runtime_memory_engine import build_runtime_memory
    from core.crypto.kaalka_runtime_engine import compute_deterministic_hash_payload

    mem = build_runtime_memory(runtime_history=[{"step": "continue", "tick": 1, "kind": "session"}])
    out = {
        "memory": mem,
        "continuation_hash": compute_deterministic_hash_payload(mem),
        "bounded": True,
    }
    return [_vector("continuation-memory", {"history": mem["runtime_history"]}, out, memory=mem)]


def probe_workflow_graph_vectors() -> list[dict[str, Any]]:
    from core.determinism.runtime_graph_parity import build_parity_runtime_graph
    from core.workflows.workflow_execution_engine import execute_workflow_plan

    plan = {"objective": "graph-probe", "steps": [{"id": "s1", "action": "extract"}]}
    executed = execute_workflow_plan(plan, tick=1)
    graph = build_parity_runtime_graph({"workflow": executed})
    out = {"execution": executed, "graph": graph, "bounded": True}
    return [_vector("workflow-graph", {"plan": plan, "tick": 1}, out, graph=graph)]


def probe_distributed_replay_vectors() -> list[dict[str, Any]]:
    from core.distributed_extraction.distributed_extraction_orchestrator import run_distributed_extraction
    from core.crypto.kaalka_hash_engine import compute_kaalka_hash_payload

    out = run_distributed_extraction([{"task_id": "r1", "url": "https://replay.test"}], None, {}, 0, [])
    replay_hash = compute_kaalka_hash_payload({"checkpoint": out.get("checkpoint"), "tick": 1})
    row = {**out, "replay_hash": replay_hash, "bounded": True}
    return [_vector("distributed-replay", {"tasks": [{"task_id": "r1", "url": "https://replay.test"}]}, row)]


def probe_runtime_identity_vectors() -> list[dict[str, Any]]:
    from core.determinism.runtime_graph_parity import build_parity_runtime_graph
    from core.reconstruction.runtime_reconstruction_engine import reconstruct_runtime

    graph = build_parity_runtime_graph({"identity": {"probe": True}})
    rebuilt = reconstruct_runtime(runtime_graph=graph, runtime_type="browser")
    out = {"runtime_id": rebuilt["runtime_id"], "graph_nodes": len(graph.get("nodes", [])), "bounded": True}
    return [_vector("runtime-identity", {"runtime_graph": graph}, out, graph=graph)]


def probe_semantic_reconciliation_vectors() -> list[dict[str, Any]]:
    from core.memory.semantic_reconciliation_memory import reconcile_memory_states

    states = [{"entities": {"a": 1}}, {"entities": {"b": 2}}]
    out = reconcile_memory_states(states)
    return [_vector("semantic-reconcile", {"states": states}, out)]


def probe_distributed_memory_vectors() -> list[dict[str, Any]]:
    from core.distributed_extraction.distributed_adaptive_runtime_engine import synchronize_adaptive_runtime

    states = [{"memory": {"healed_selectors": {"#x": "ok"}, "pagination_patterns": ["p"]}}]
    out = synchronize_adaptive_runtime(states)
    return [_vector("distributed-memory", {"states": states}, out)]


def probe_orchestration_vectors() -> list[dict[str, Any]]:
    from core.orchestration.orchestration_engine import orchestrate

    out = orchestrate("https://orch.test")
    return [_vector("orchestration-extract", {"seed": "https://orch.test"}, out)]


PROBE_FAMILIES: dict[str, Callable[[], list[dict[str, Any]]]] = {
    "runtime_vectors": probe_runtime_vectors,
    "graph_vectors": probe_graph_vectors,
    "semantic_vectors": probe_semantic_vectors,
    "vm_vectors": probe_vm_vectors,
    "replay_vectors": probe_replay_vectors,
    "distributed_vectors": probe_distributed_vectors,
    "workflow_vectors": probe_workflow_vectors,
    "memory_vectors": probe_memory_vectors,
    "repository_vectors": probe_repository_vectors,
    "browser_vectors": probe_browser_vectors,
    "continuation_vectors": probe_continuation_vectors,
    "parser_vectors": probe_parser_vectors,
    "reconstruction_vectors": probe_reconstruction_vectors,
    "ontology_vectors": probe_ontology_vectors,
    "continuation_memory_vectors": probe_continuation_memory_vectors,
    "workflow_graph_vectors": probe_workflow_graph_vectors,
    "distributed_replay_vectors": probe_distributed_replay_vectors,
    "runtime_identity_vectors": probe_runtime_identity_vectors,
    "semantic_reconciliation_vectors": probe_semantic_reconciliation_vectors,
    "distributed_memory_vectors": probe_distributed_memory_vectors,
    "orchestration_vectors": probe_orchestration_vectors,
}


def all_vectors() -> dict[str, list[dict[str, Any]]]:
    return {name: fn() for name, fn in PROBE_FAMILIES.items()}


def write_vectors() -> Path:
    VECTORS.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat()
    for family, vectors in all_vectors().items():
        dest = VECTORS / family
        dest.mkdir(parents=True, exist_ok=True)
        payload = {
            "family": family,
            "generated_at": ts,
            "source": "origin/python",
            "algorithm": "webweavex-canonical-probes@2.0.0",
            "vectors": vectors,
        }
        (dest / "canonical.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return VECTORS
