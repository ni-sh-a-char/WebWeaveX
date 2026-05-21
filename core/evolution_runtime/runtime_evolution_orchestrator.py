from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.evolution_runtime.runtime_adaptation_engine import adapt_runtime_strategy
from core.evolution_runtime.runtime_convergence_engine import converge_runtime_evolution
from core.evolution_runtime.runtime_diff_engine import diff_evolution_runtime
from core.evolution_runtime.runtime_evolution_engine import build_runtime_evolution
from core.evolution_runtime.runtime_evolution_graph_engine import build_runtime_evolution_graph
from core.evolution_runtime.runtime_lineage_engine import build_runtime_lineage
from core.evolution_runtime.runtime_memory_engine import load_evolution_runtime
from core.evolution_runtime.runtime_memory_engine import remember_evolution_runtime
from core.evolution_runtime.runtime_memory_engine import save_evolution_runtime
from core.evolution_runtime.runtime_mutation_engine import build_runtime_mutations
from core.evolution_runtime.runtime_optimization_engine import optimize_runtime_execution
from core.evolution_runtime.runtime_pattern_engine import build_runtime_patterns
from core.evolution_runtime.runtime_policy_engine import build_runtime_policy
from core.evolution_runtime.runtime_policy_engine import enforce_runtime_policy
from core.evolution_runtime.runtime_recovery_evolution_engine import evolve_recovery_order
from core.evolution_runtime.runtime_repair_engine import repair_runtime_failures
from core.evolution_runtime.runtime_strategy_engine import build_runtime_strategy
from core.evolution_runtime.selector_evolution_engine import evolve_selector_runtime
from core.evolution_runtime.semantic_evolution_engine import evolve_semantic_runtime
from core.evolution_runtime.topology_evolution_engine import evolve_runtime_topology
from core.evolution_runtime.workflow_evolution_engine import evolve_workflow_runtime
from core.ir.evolution_runtime_ir import (
    compile_evolution_runtime_ir,
    evolution_runtime_ir_to_graph,
)


def run_evolution_runtime(
    adaptive_memory: Optional[Dict[str, Any]] = None,
    workflow_result: Optional[Dict[str, Any]] = None,
    semantic_result: Optional[Dict[str, Any]] = None,
    sync_result: Optional[Dict[str, Any]] = None,
    distributed_result: Optional[Dict[str, Any]] = None,
    failures: Optional[List[str]] = None,
    memory: Optional[Dict[str, Any]] = None,
    tick: int = 0,
) -> Dict[str, Any]:
    memory = dict(memory or {})
    adaptive_memory = adaptive_memory or {}
    failures = failures or []

    healed = dict(adaptive_memory.get("healed_selectors", {}))
    selector = evolve_selector_runtime(
        adaptive_memory.get("selectors", {}),
        healed,
    )

    workflow_inner = (workflow_result or {}).get("workflow", workflow_result or {})
    workflow = evolve_workflow_runtime(
        workflow_inner.get("plan", {}),
        workflow_inner.get("execution", {}),
        memory.get("evolution_histories", []),
    )

    semantic = evolve_semantic_runtime(
        semantic_result,
        memory.get("evolution_histories", []),
    )

    sync_inner = (sync_result or {}).get("synchronization", sync_result or {})
    topology = evolve_runtime_topology(
        (distributed_result or {}).get("workers", []),
        sync_inner,
        (sync_result or {}).get("causality"),
    )

    evidence = {
        "drift_count": len(sync_inner.get("drift", {}).get("drifts", [])),
        "failed_steps": failures.count("failed_workflow"),
    }
    strategy = build_runtime_strategy(evidence)
    repairs = repair_runtime_failures(failures, healed)
    recovery = evolve_recovery_order(repairs.get("repairs", []))

    depth = len(workflow.get("execution_ordering", []))
    optimization = optimize_runtime_execution(
        depth=depth,
        replay_cost=len(memory.get("evolution_histories", [])),
        sync_overhead=len(sync_inner.get("deltas", [])),
    )
    adapted_strategy = adapt_runtime_strategy(strategy, optimization)

    mutations = build_runtime_mutations(
        selector,
        workflow,
        semantic,
        sync_inner.get("convergence", {}),
    )
    parent_id = str(memory.get("last_evolution_id", ""))
    lineage = build_runtime_lineage("", mutations, parent_id)
    evolution = build_runtime_evolution(mutations, lineage)
    evolution["evolution_id"] = evolution["evolution_id"]
    lineage = build_runtime_lineage(evolution["evolution_id"], mutations, parent_id)

    policy = build_runtime_policy()
    enforcement = enforce_runtime_policy(
        policy,
        mutations,
        repairs.get("repairs", []),
        depth,
    )

    patterns = build_runtime_patterns(
        ui=(semantic_result or {}).get("semantic", {}).get("ui", {}),
        workflows=[workflow_inner.get("plan", {})],
        semantic=semantic_result,
        sync_history=memory.get("evolution_histories", []),
    )

    graph = build_runtime_evolution_graph(evolution, repairs, optimization)

    prior = memory.get("last_evolution", {})
    diff = diff_evolution_runtime(prior, evolution) if prior else {"revertible": True}

    distributed_evolutions = [evolution]
    if memory.get("distributed_evolutions"):
        distributed_evolutions.extend(memory["distributed_evolutions"])
    convergence = converge_runtime_evolution(distributed_evolutions)

    payload = {
        "evolution": evolution,
        "selector": selector,
        "workflow": workflow,
        "semantic": semantic,
        "topology": topology,
        "strategy": adapted_strategy,
        "repairs": repairs,
        "recovery": recovery,
        "optimization": optimization,
        "patterns": patterns,
        "lineage": lineage,
        "graph": graph,
        "policy": policy,
        "enforcement": enforcement,
        "convergence": convergence,
        "diff": diff,
        "tick": tick,
        "bounded": True,
    }

    updated_memory = remember_evolution_runtime(
        memory,
        {
            "evolution_histories": list(memory.get("evolution_histories", [])) + [evolution],
            "selector_lineage": lineage,
            "workflow_evolution": workflow,
            "semantic_evolution": semantic,
            "optimization_histories": list(memory.get("optimization_histories", [])) + [optimization],
            "last_evolution": evolution,
            "last_evolution_id": evolution["evolution_id"],
            "distributed_evolutions": distributed_evolutions[-10:],
        },
    )
    payload["memory"] = updated_memory
    payload["replay"] = {
        "lineage": lineage,
        "evolution": evolution,
        "replayed": True,
        "bounded": True,
    }
    payload["evolution_ir"] = compile_evolution_runtime_ir(payload)
    return payload


def run_evolution_for_extraction(
    evolving_runtime: bool = True,
    memory_path: str = "",
    memory_key: str = "",
    adaptive_memory: Optional[Dict[str, Any]] = None,
    workflow_result: Optional[Dict[str, Any]] = None,
    semantic_result: Optional[Dict[str, Any]] = None,
    sync_result: Optional[Dict[str, Any]] = None,
    distributed_result: Optional[Dict[str, Any]] = None,
    failures: Optional[List[str]] = None,
    tick: int = 0,
    merge_graph: bool = True,
) -> Dict[str, Any]:
    if not evolving_runtime:
        return {"enabled": False, "bounded": True}

    memory: Dict[str, Any] = {}
    if memory_path and memory_key:
        loaded = load_evolution_runtime(memory_path, memory_key)
        if loaded.get("available"):
            memory = loaded.get("memory", memory)

    result = run_evolution_runtime(
        adaptive_memory=adaptive_memory,
        workflow_result=workflow_result,
        semantic_result=semantic_result,
        sync_result=sync_result,
        distributed_result=distributed_result,
        failures=failures,
        memory=memory,
        tick=tick,
    )

    persisted = False
    if memory_path and memory_key:
        save_evolution_runtime(memory_path, result.get("memory", {}), memory_key)
        persisted = True

    graph_ir = evolution_runtime_ir_to_graph(result.get("evolution_ir", {}))
    unified_graph = {}
    if merge_graph:
        from core.runtime_graph.runtime_graph_engine import build_runtime_graph

        unified_graph = build_runtime_graph([graph_ir])

    return {
        "enabled": True,
        "evolution": result,
        "evolution_ir": result.get("evolution_ir", {}),
        "evolution_graph_ir": graph_ir,
        "unified_graph": unified_graph,
        "replay": result.get("replay", {}),
        "memory_persisted": persisted,
        "bounded": True,
    }
