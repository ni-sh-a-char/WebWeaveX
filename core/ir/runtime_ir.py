from __future__ import annotations

from typing import Any, Dict, List

from core.ir.execution_ir import compile_execution_ir
from core.ir.topology_ir import compile_topology_ir
from core.ssa import build_ssa_form
from core.ssa.multilang_ssa_engine import build_multilang_ssa
from core.runtime.event_stream_engine import reconstruct_event_stream
from core.runtime.distributed_topology_engine import build_distributed_topology
from core.runtime.distributed_partition_engine import partition_runtime_graph
from core.runtime.runtime_simulation_engine import simulate_runtime_execution
from core.runtime.execution_graph_reconciliation_engine import reconcile_execution_graphs
from core.runtime.semantic_replay_vm import replay_semantic_events
from core.runtime.topology_runtime_convergence_engine import converge_runtime_and_topology
from core.runtime.execution_optimizer_engine import optimize_execution_order
from core.runtime.semantic_cache_engine import SemanticCache
from core.treesitter import parse_universal_ast, detect_language
from core.treesitter.tree_sitter_loader import create_parser
from core.optimizer import optimize_semantic_ir
from core.persistence import persist_semantic_ir
from core.query.semantic_query_planner_v2 import build_query_plan
from core.bytecode import compile_semantic_bytecode
from core.vm import SemanticVirtualMachine
from core.transactions.semantic_transaction_engine import SemanticTransaction
from core.runtime.semantic_journal_engine import SemanticJournal
from core.runtime.semantic_dependency_resolver import resolve_dependencies
from core.persistence.semantic_graph_storage_engine import SemanticGraphStorage
from core.hypergraph import build_semantic_hypergraph
from core.database.semantic_graph_database import SemanticGraphDatabase
from core.database.semantic_wal_engine import SemanticWAL
from core.runtime.distributed_worker_engine import assign_distributed_workers
from core.compiler import compile_semantic_pipeline, compile_execution_plan
from core.distributed import schedule_distributed_execution, create_distributed_checkpoint
from core.query.semantic_query_execution_engine import execute_semantic_query
from core.query_language import (
    parse_semantic_query,
    build_query_ast,
    plan_semantic_query,
    optimize_semantic_query,
    execute_semantic_plan,
)
from core.distributed.distributed_dag_execution_engine import execute_semantic_dag
from core.distributed.distributed_execution_coordinator import coordinate_distributed_execution
from core.runtime.semantic_resource_accounting_engine import account_semantic_resources
from core.agents import SemanticAgent, SemanticAgentRuntime, build_semantic_task_graph
from core.runtime.semantic_event_bus_engine import SemanticEventBus
from core.distributed.semantic_service_mesh_engine import build_semantic_service_mesh
from core.distributed.semantic_cluster_orchestrator import orchestrate_semantic_cluster
from core.runtime.semantic_resource_scheduler import schedule_semantic_resources
from core.runtime.semantic_runtime_policy_engine import enforce_runtime_policy
from core.runtime.semantic_security_boundary_engine import validate_semantic_boundary
from core.runtime.distributed_routing_engine import route_semantic_tasks
from core.runtime.semantic_snapshot_engine_v2 import create_runtime_snapshot
from core.runtime.semantic_consistency_proof_engine import prove_runtime_consistency as prove_semantic_runtime_consistency
from core.actors import SemanticActorSystem
from core.crdt.semantic_crdt_engine import merge_semantic_states
from core.distributed_memory.semantic_memory_fabric import SemanticMemoryFabric
from core.consensus.semantic_consensus_engine import compute_semantic_consensus
from core.stream.semantic_stream_engine import SemanticStream
from core.filesystem.semantic_filesystem_engine import SemanticFilesystem
from core.distributed_memory.semantic_replication_engine import replicate_semantic_region
from core.transactions.distributed_transaction_coordinator import coordinate_transactions
from core.runtime.cluster_state_engine import compute_cluster_state
from core.runtime.distributed_cache_engine import DistributedSemanticCache
from core.world_model import (
    analyze_semantic_impact,
    build_repository_world_model,
    build_semantic_architecture_graph,
)
from core.autonomy import (
    orchestrate_semantic_runtime,
)
from core.evolution import (
    orchestrate_semantic_evolution,
)
from core.engineering import (
    orchestrate_semantic_engineering,
)
from core.execution_reality import (
    orchestrate_execution_reality,
)
from core.causal_intelligence import (
    orchestrate_semantic_causal_intelligence,
)
from core.execution_physics import (
    orchestrate_execution_physics,
)

RuntimeIR = Dict[str, Any]


def _extract_services(execution: Dict[str, Any]) -> List[str]:
    services: List[str] = []
    for s in execution.get("services", []):
        if isinstance(s, dict):
            name = s.get("name") or s.get("id")
            if name:
                services.append(str(name))
        elif s:
            services.append(str(s))
    return sorted(services) if services else ["default"]


def compile_runtime_ir(source: str = "", graph: Dict[str, Any] | None = None, path: str = "") -> RuntimeIR:
    execution = compile_execution_ir(source, path)
    g = graph or {}
    topology = compile_topology_ir(g or {"nodes": [], "edges": execution.get("topology", [])})

    services = _extract_services(execution)
    events: List[Dict[str, Any]] = list(g.get("events", []) or [])
    transitions: List[Dict[str, Any]] = list(g.get("transitions", []) or [])

    try:
        ssa = build_ssa_form(source or "pass")
    except SyntaxError:
        ssa = {
            "ssa_assignments": [],
            "variable_versions": {},
            "bounded": True,
            "deterministic": True,
        }

    lang = detect_language(path or "main.py") or "python"
    multilang_ssa = build_multilang_ssa(source or "", lang)
    tree_sitter = create_parser(lang) if lang else {"available": False}

    event_stream = reconstruct_event_stream(events)
    distributed_topology = build_distributed_topology(services)

    universal_ast = parse_universal_ast(source or "", path or "main.py")
    semantic_ir = universal_ast.get("ir", {})
    if not isinstance(semantic_ir, dict):
        semantic_ir = {}

    optimized_semantic_ir = optimize_semantic_ir(dict(semantic_ir))

    runtime_simulation = simulate_runtime_execution(transitions)
    semantic_replay = replay_semantic_events(events)

    topology_nodes: List[Dict[str, Any]] = list(g.get("nodes", []) or [])
    if not topology_nodes:
        topology_nodes = [{"id": s, "type": "service"} for s in services]
    topology_graph = {"nodes": topology_nodes}

    execution_reconciliation = reconcile_execution_graphs(
        distributed_topology,
        topology_graph,
    )

    runtime_partial = {
        "distributed_topology": distributed_topology,
        "ssa": ssa,
        "event_stream": event_stream,
    }
    topology_convergence = converge_runtime_and_topology(
        runtime_partial,
        topology_graph,
    )

    distributed_partitions = partition_runtime_graph(topology_nodes)

    persistence = persist_semantic_ir(
        {
            "execution": execution,
            "topology": topology,
            "ssa": ssa,
            "distributed_topology": distributed_topology,
        }
    )

    execution_optimizer = optimize_execution_order(list(g.get("tasks", []) or []))
    query_plan = build_query_plan({"type": "runtime"})
    cache = SemanticCache()
    cache_key = cache.put({"source": source}, optimized_semantic_ir)

    bytecode_ir = dict(optimized_semantic_ir)
    bytecode_ir["edges"] = list(distributed_topology.get("edges", [])) + list(
        event_stream.get("edges", [])
    )
    bytecode = compile_semantic_bytecode(bytecode_ir)
    vm = SemanticVirtualMachine()
    vm_result = vm.execute(bytecode["instructions"])
    transaction = SemanticTransaction()
    transaction.add_operation({"type": "runtime_compile"})
    transaction_result = transaction.commit()
    journal = SemanticJournal()
    journal.record({"event": "runtime_ir_compiled"})
    journal_state = journal.replay()
    dependency_resolution = resolve_dependencies(list(g.get("tasks", []) or []))
    graph_storage = SemanticGraphStorage()
    for node in topology_nodes:
        if isinstance(node, dict) and node.get("id"):
            graph_storage.add_node(node)
    for edge in bytecode_ir.get("edges", []):
        if isinstance(edge, dict):
            graph_storage.add_edge(edge)
    graph_snapshot = graph_storage.snapshot()

    topo_nodes = distributed_topology.get("nodes", [])
    member_ids = sorted(
        n.get("id") for n in topo_nodes if isinstance(n, dict) and n.get("id")
    )
    hypergraph_rels = []
    if len(member_ids) >= 2:
        hypergraph_rels.append(
            {
                "type": "runtime_cluster",
                "members": member_ids,
            }
        )
    hypergraph = build_semantic_hypergraph(
        nodes=topo_nodes,
        relationships=hypergraph_rels,
    )

    graph_db = SemanticGraphDatabase()
    for node in topo_nodes:
        if isinstance(node, dict):
            graph_db.insert_node(node)
    for edge in distributed_topology.get("edges", []):
        if isinstance(edge, dict):
            graph_db.insert_edge(edge)
    graph_db_stats = graph_db.stats()

    wal = SemanticWAL()
    wal.append({"event": "runtime_compiled"})
    wal_state = wal.replay()

    worker_assignments = assign_distributed_workers(list(g.get("tasks", []) or []))
    execution_plan = compile_execution_plan(bytecode_ir)
    routing = route_semantic_tasks(
        tasks=list(g.get("tasks", []) or []),
        nodes=topo_nodes or topology_nodes,
    )
    runtime_snapshot = create_runtime_snapshot(
        {
            "vm": vm_result,
            "journal": journal_state,
        }
    )
    runtime_consistency = prove_semantic_runtime_consistency(vm_result)

    actor_system = SemanticActorSystem()
    actor_system.create_actor("runtime")
    actor_system.send("runtime", {"event": "boot"})
    actor_message = actor_system.receive("runtime")

    memory_fabric = SemanticMemoryFabric()
    memory_fabric.put("runtime", "snapshot", runtime_snapshot)
    memory_value = memory_fabric.get("runtime", "snapshot")

    consensus = compute_semantic_consensus(
        [{"value": "stable"}, {"value": "stable"}]
    )

    stream = SemanticStream()
    stream.push({"event": "runtime_start"})
    stream_event = stream.next()

    filesystem = SemanticFilesystem()
    filesystem.write("/runtime/state", "active")

    replication = replicate_semantic_region(state=runtime_snapshot, replicas=3)

    transaction_coordination = coordinate_transactions([{"id": "tx1"}])

    cluster_state = compute_cluster_state(distributed_topology.get("nodes", []))

    distributed_cache = DistributedSemanticCache()
    distributed_cache_key = distributed_cache.put(runtime_snapshot)
    cached_snapshot = distributed_cache.get(distributed_cache_key)

    crdt_state = merge_semantic_states({"a": 1}, {"a": 2})

    compiler_pipeline = compile_semantic_pipeline(bytecode_ir)
    schedule_nodes = sorted(
        str(n.get("id"))
        for n in topo_nodes
        if isinstance(n, dict) and n.get("id")
    ) or ["node_a", "node_b"]
    distributed_schedule = schedule_distributed_execution(
        tasks=compiler_pipeline.get("execution_plan", {}).get("plan", []),
        nodes=schedule_nodes,
    )
    distributed_checkpoint = create_distributed_checkpoint(compiler_pipeline)
    semantic_query = execute_semantic_query(
        nodes=distributed_topology.get("nodes", []),
        filters={},
    )

    parsed_query = parse_semantic_query("SELECT id WHERE type = service LIMIT 10")
    query_ast = build_query_ast(parsed_query)
    semantic_query_plan = plan_semantic_query(query_ast)
    optimized_query_plan = optimize_semantic_query(semantic_query_plan)
    query_execution = execute_semantic_plan(
        optimized_query_plan,
        dataset=distributed_topology.get("nodes", []),
    )
    dag_execution = execute_semantic_dag(distributed_topology.get("nodes", []))
    resource_accounting = account_semantic_resources(optimized_semantic_ir)
    execution_coordination = coordinate_distributed_execution(
        [distributed_schedule]
    )

    agent_runtime = SemanticAgentRuntime()
    runtime_agent = SemanticAgent(
        agent_id="runtime",
        capabilities=["execute"],
    )
    agent_runtime.register(runtime_agent)
    boot_payload = {"task": "boot"}
    boundary = validate_semantic_boundary(boot_payload)
    agent_result = (
        agent_runtime.execute("runtime", boot_payload)
        if boundary.get("accepted")
        else {"status": "blocked", "agent_id": "runtime"}
    )
    task_graph = build_semantic_task_graph(list(g.get("tasks", []) or []))
    platform_event_bus = SemanticEventBus()
    platform_event_bus.publish({"event": "runtime_boot"})
    service_mesh = build_semantic_service_mesh(distributed_topology.get("nodes", []))
    semantic_cluster = orchestrate_semantic_cluster(distributed_topology.get("nodes", []))
    platform_resource_schedule = schedule_semantic_resources(list(g.get("tasks", []) or []))
    runtime_policy = enforce_runtime_policy({"compiler": True, "query": True})

    repository_irs: List[Dict[str, Any]] = list(
        g.get("repository_irs", []) or []
    )
    if not repository_irs and path:
        repository_irs = [
            {
                "path": path,
                "semantic_ast": semantic_ir,
            }
        ]

    repository_world_model = build_repository_world_model(
        repository_irs
    )
    architecture_graph = build_semantic_architecture_graph(
        repository_irs
    )
    impact_analysis = analyze_semantic_impact(
        path,
        architecture_graph,
    )

    semantic_autonomy = orchestrate_semantic_runtime(
        {
            "goal": path or "compile_runtime",
        }
    )

    evolution_context = dict(semantic_autonomy)
    evolution_context["architecture_graph"] = architecture_graph
    evolution_context["repository_world_model"] = repository_world_model

    semantic_evolution = orchestrate_semantic_evolution(
        evolution_context
    )

    engineering_context = dict(semantic_evolution)
    engineering_context["distributed_topology"] = distributed_topology
    engineering_context["transitions"] = list(
        g.get("transitions", []) or []
    )
    engineering_context["graph_database"] = graph_db_stats
    engineering_context["events"] = events
    engineering_context["repository_world_model"] = repository_world_model

    semantic_engineering = orchestrate_semantic_engineering(
        engineering_context
    )

    execution_reality_context = {
        "distributed_topology": distributed_topology,
        "transitions": transitions,
        "event_stream": event_stream,
        "semantic_crdt": crdt_state,
        "tasks": list(g.get("tasks", []) or []),
        "distributed_workers": worker_assignments.get(
            "assignments",
            [],
        ),
        "journal": journal_state,
    }

    semantic_execution_reality = orchestrate_execution_reality(
        execution_reality_context
    )

    causal_intelligence_context = {
        "distributed_topology": distributed_topology,
        "transitions": transitions,
        "event_stream": event_stream,
        "runtime_entropy": semantic_execution_reality.get(
            "runtime_entropy",
            {},
        ),
        "execution_pressure": semantic_execution_reality.get(
            "execution_pressure",
            {},
        ),
        "runtime_conflicts": semantic_execution_reality.get(
            "runtime_conflicts",
            {},
        ),
        "journal": journal_state,
        "tasks": list(g.get("tasks", []) or []),
        "distributed_workers": worker_assignments.get(
            "assignments",
            [],
        ),
    }

    semantic_causal_intelligence = orchestrate_semantic_causal_intelligence(
        causal_intelligence_context
    )

    execution_physics_context = {
        "distributed_topology": distributed_topology,
        "transitions": transitions,
        "events": list(
            event_stream.get(
                "events",
                [],
            )
            if isinstance(event_stream, dict)
            else []
        ),
        "distributed_workers": worker_assignments.get(
            "assignments",
            [],
        ),
        "runtime_entropy": semantic_execution_reality.get(
            "runtime_entropy",
            {},
        ),
        "journal": journal_state,
        "tasks": list(g.get("tasks", []) or []),
        "runtime_conflicts": semantic_execution_reality.get(
            "runtime_conflicts",
            {},
        ),
        "state_convergence": semantic_causal_intelligence.get(
            "runtime_equilibrium",
            {},
        ),
    }

    semantic_execution_physics = orchestrate_execution_physics(
        execution_physics_context
    )

    return {
        "execution": execution,
        "topology": topology,
        "ssa": ssa,
        "multilang_ssa": multilang_ssa,
        "tree_sitter": {
            "available": tree_sitter.get("available", False),
            "language": lang,
            "reason": tree_sitter.get("reason"),
        },
        "event_stream": event_stream,
        "distributed_topology": distributed_topology,
        "distributed_partitions": distributed_partitions,
        "universal_ast": universal_ast,
        "semantic_ir": semantic_ir,
        "optimized_semantic_ir": optimized_semantic_ir,
        "runtime_simulation": runtime_simulation,
        "semantic_replay": semantic_replay,
        "execution_reconciliation": execution_reconciliation,
        "topology_convergence": topology_convergence,
        "execution_optimizer": execution_optimizer,
        "query_plan": query_plan,
        "cache_key": cache_key,
        "persistence": persistence,
        "semantic_bytecode": bytecode,
        "semantic_vm": vm_result,
        "transaction": transaction_result,
        "journal": journal_state,
        "dependency_resolution": dependency_resolution,
        "graph_storage": graph_snapshot,
        "semantic_hypergraph": hypergraph,
        "graph_database": graph_db_stats,
        "semantic_wal": wal_state,
        "distributed_workers": worker_assignments,
        "execution_plan": execution_plan,
        "distributed_routing": routing,
        "runtime_snapshot_v2": runtime_snapshot,
        "runtime_consistency": runtime_consistency,
        "semantic_actor_message": actor_message,
        "semantic_memory_fabric": memory_value,
        "semantic_consensus": consensus,
        "semantic_stream_event": stream_event,
        "semantic_filesystem": filesystem.list_paths(),
        "semantic_replication": replication,
        "transaction_coordination": transaction_coordination,
        "cluster_state": cluster_state,
        "distributed_cache_key": distributed_cache_key,
        "distributed_cached_snapshot": cached_snapshot,
        "semantic_crdt": crdt_state,
        "compiler_pipeline": compiler_pipeline,
        "distributed_schedule": distributed_schedule,
        "distributed_checkpoint": distributed_checkpoint,
        "semantic_query": semantic_query,
        "query_ast": query_ast,
        "query_plan_v2": optimized_query_plan,
        "query_execution": query_execution,
        "dag_execution": dag_execution,
        "resource_accounting": resource_accounting,
        "execution_coordination": execution_coordination,
        "semantic_agent": agent_result,
        "semantic_task_graph": task_graph,
        "semantic_service_mesh": service_mesh,
        "semantic_cluster": semantic_cluster,
        "platform_resource_schedule": platform_resource_schedule,
        "runtime_policy": runtime_policy,
        "security_boundary": boundary,
        "repository_world_model": repository_world_model,
        "semantic_architecture_graph": architecture_graph,
        "semantic_impact_analysis": impact_analysis,
        "semantic_autonomy": semantic_autonomy,
        "semantic_evolution": semantic_evolution,
        "semantic_engineering": semantic_engineering,
        "semantic_execution_reality": semantic_execution_reality,
        "semantic_causal_intelligence": semantic_causal_intelligence,
        "semantic_execution_physics": semantic_execution_physics,
        "bounded": True,
        "deterministic": True,
    }
