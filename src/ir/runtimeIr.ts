/**
 * Converted from Python: core/ir/runtime_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileExecutionIr } from "./executionIr.js";
import { compileTopologyIr } from "./topologyIr.js";
import { buildSsaForm } from "../ssa/index.js";
import { buildMultilangSsa } from "../ssa/multilangSsaEngine.js";
import { reconstructEventStream } from "../runtime/eventStreamEngine.js";
import { buildDistributedTopology } from "../runtime/distributedTopologyEngine.js";
import { partitionRuntimeGraph } from "../runtime/distributedPartitionEngine.js";
import { simulateRuntimeExecution } from "../runtime/runtimeSimulationEngine.js";
import { reconcileExecutionGraphs } from "../runtime/executionGraphReconciliationEngine.js";
import { replaySemanticEvents } from "../runtime/semanticReplayVm.js";
import { convergeRuntimeAndTopology } from "../runtime/topologyRuntimeConvergenceEngine.js";
import { optimizeExecutionOrder } from "../runtime/executionOptimizerEngine.js";
import { SemanticCache } from "../runtime/semanticCacheEngine.js";
import { parseUniversalAst, detectLanguage } from "../treesitter/index.js";
import { createParser } from "../treesitter/treeSitterLoader.js";
import { optimizeSemanticIr } from "../optimizer/index.js";
import { persistSemanticIr } from "../persistence/index.js";
import { buildQueryPlan } from "../query/semanticQueryPlannerV2.js";
import { compileSemanticBytecode } from "../bytecode/index.js";
import { SemanticVirtualMachine } from "../vm/index.js";
import { SemanticTransaction } from "../transactions/semanticTransactionEngine.js";
import { SemanticJournal } from "../runtime/semanticJournalEngine.js";
import { resolveDependencies } from "../runtime/semanticDependencyResolver.js";
import { SemanticGraphStorage } from "../persistence/semanticGraphStorageEngine.js";
import { buildSemanticHypergraph } from "../hypergraph/index.js";
import { SemanticGraphDatabase } from "../database/semanticGraphDatabase.js";
import { SemanticWAL } from "../database/semanticWalEngine.js";
import { assignDistributedWorkers } from "../runtime/distributedWorkerEngine.js";
import { compileSemanticPipeline, compileExecutionPlan } from "../compiler/index.js";
import { scheduleDistributedExecution, createDistributedCheckpoint } from "../distributed/index.js";
import { executeSemanticQuery } from "../query/semanticQueryExecutionEngine.js";
import { parseSemanticQuery, buildQueryAst, planSemanticQuery, optimizeSemanticQuery, executeSemanticPlan } from "../query_language/index.js";
import { executeSemanticDag } from "../distributed/distributedDagExecutionEngine.js";
import { coordinateDistributedExecution } from "../distributed/distributedExecutionCoordinator.js";
import { accountSemanticResources } from "../runtime/semanticResourceAccountingEngine.js";
import { SemanticAgent, SemanticAgentRuntime, buildSemanticTaskGraph } from "../agents/index.js";
import { SemanticEventBus } from "../runtime/semanticEventBusEngine.js";
import { buildSemanticServiceMesh } from "../distributed/semanticServiceMeshEngine.js";
import { orchestrateSemanticCluster } from "../distributed/semanticClusterOrchestrator.js";
import { scheduleSemanticResources } from "../runtime/semanticResourceScheduler.js";
import { enforceRuntimePolicy } from "../runtime/semanticRuntimePolicyEngine.js";
import { validateSemanticBoundary } from "../runtime/semanticSecurityBoundaryEngine.js";
import { routeSemanticTasks } from "../runtime/distributedRoutingEngine.js";
import { createRuntimeSnapshot } from "../runtime/semanticSnapshotEngineV2.js";
import { proveRuntimeConsistency as proveSemanticRuntimeConsistency } from "../runtime/semanticConsistencyProofEngine.js";
import { SemanticActorSystem } from "../actors/index.js";
import { mergeSemanticStates } from "../crdt/semanticCrdtEngine.js";
import { SemanticMemoryFabric } from "../distributed_memory/semanticMemoryFabric.js";
import { computeSemanticConsensus } from "../consensus/semanticConsensusEngine.js";
import { SemanticStream } from "../stream/semanticStreamEngine.js";
import { SemanticFilesystem } from "../filesystem/semanticFilesystemEngine.js";
import { replicateSemanticRegion } from "../distributed_memory/semanticReplicationEngine.js";
import { coordinateTransactions } from "../transactions/distributedTransactionCoordinator.js";
import { computeClusterState } from "../runtime/clusterStateEngine.js";
import { DistributedSemanticCache } from "../runtime/distributedCacheEngine.js";
import { analyzeSemanticImpact, buildRepositoryWorldModel, buildSemanticArchitectureGraph } from "../world_model/index.js";
import { orchestrateSemanticRuntime } from "../autonomy/index.js";
import { orchestrateSemanticEvolution } from "../evolution/index.js";
import { orchestrateSemanticEngineering } from "../engineering/index.js";
import { orchestrateExecutionReality } from "../execution_reality/index.js";
import { orchestrateSemanticCausalIntelligence } from "../causal_intelligence/index.js";
import { orchestrateExecutionPhysics } from "../execution_physics/index.js";

export let RuntimeIR: any = py.at(Object, [py.toStr, Object]);
export function _extractServices(execution: any): any {
  var services: any[] = [];
  var s: any;
  for (s of py.iter(py.get(execution, "services", []))) {
    if (((s !== null && typeof s === "object" && !Array.isArray(s) && !(s instanceof Set) && !(s instanceof Map)))) {
      var name: any = py.or2(py.get(s, "name"), () => (py.get(s, "id")));
      if (py.truthy(name)) {
        py.listAppend(services, py.toStr(name));
      }
    } else if (py.truthy(s)) {
      py.listAppend(services, py.toStr(s));
    }
  }
  return (py.truthy(services) ? py.sorted(services) : ["default"]);
}
export function compileRuntimeIr(source: any = "", graph: any = null, path: any = ""): any {
  var execution: any = compileExecutionIr(source, path);
  var g: any = py.or2(graph, () => ({}));
  var topology: any = compileTopologyIr(py.or2(g, () => ({"nodes": [], "edges": py.get(execution, "topology", [])})));
  var services: any = _extractServices(execution);
  var events: any = [...py.iter(py.or2(py.get(g, "events", []), () => ([])))];
  var transitions: any = [...py.iter(py.or2(py.get(g, "transitions", []), () => ([])))];
  try {
    var ssa: any = buildSsaForm(py.or2(source, () => ("pass")));
  } catch (_e: any) {
    ssa = {"ssa_assignments": [], "variable_versions": {}, "bounded": true, "deterministic": true};
  }
  var lang: any = py.or2(detectLanguage(py.or2(path, () => ("main.py"))), () => ("python"));
  var multilang_ssa: any = buildMultilangSsa(py.or2(source, () => ("")), lang);
  var tree_sitter: any = (py.truthy(lang) ? createParser(lang) : {"available": false});
  var event_stream: any = reconstructEventStream(events);
  var distributed_topology: any = buildDistributedTopology(services);
  var universal_ast: any = parseUniversalAst(py.or2(source, () => ("")), py.or2(path, () => ("main.py")));
  var semantic_ir: any = py.get(universal_ast, "ir", {});
  if (!((semantic_ir !== null && typeof semantic_ir === "object" && !Array.isArray(semantic_ir) && !(semantic_ir instanceof Set) && !(semantic_ir instanceof Map)))) {
    semantic_ir = {};
  }
  var optimized_semantic_ir: any = optimizeSemanticIr(py.pyDict(semantic_ir));
  var runtime_simulation: any = simulateRuntimeExecution(transitions);
  var semantic_replay: any = replaySemanticEvents(events);
  var topology_nodes: any = [...py.iter(py.or2(py.get(g, "nodes", []), () => ([])))];
  if (!py.truthy(topology_nodes)) {
    topology_nodes = py.iter(services).map((s: any) => ({"id": s, "type": "service"}));
  }
  var topology_graph: any = {"nodes": topology_nodes};
  var execution_reconciliation: any = reconcileExecutionGraphs(distributed_topology, topology_graph);
  var runtime_partial: any = {"distributed_topology": distributed_topology, "ssa": ssa, "event_stream": event_stream};
  var topology_convergence: any = convergeRuntimeAndTopology(runtime_partial, topology_graph);
  var distributed_partitions: any = partitionRuntimeGraph(topology_nodes);
  var persistence: any = persistSemanticIr({"execution": execution, "topology": topology, "ssa": ssa, "distributed_topology": distributed_topology});
  var execution_optimizer: any = optimizeExecutionOrder([...py.iter(py.or2(py.get(g, "tasks", []), () => ([])))]);
  var query_plan: any = buildQueryPlan({"type": "runtime"});
  var cache: any = new SemanticCache();
  var cache_key: any = cache.put({"source": source}, optimized_semantic_ir);
  var bytecode_ir: any = py.pyDict(optimized_semantic_ir);
  py.setItem(bytecode_ir, "edges", py.add([...py.iter(py.get(distributed_topology, "edges", []))], [...py.iter(py.get(event_stream, "edges", []))]));
  var bytecode: any = compileSemanticBytecode(bytecode_ir);
  var vm: any = new SemanticVirtualMachine();
  var vm_result: any = vm.execute(py.at(bytecode, "instructions"));
  var transaction: any = new SemanticTransaction();
  transaction.add_operation({"type": "runtime_compile"});
  var transaction_result: any = transaction.commit();
  var journal: any = new SemanticJournal();
  journal.record({"event": "runtime_ir_compiled"});
  var journal_state: any = journal.replay();
  var dependency_resolution: any = resolveDependencies([...py.iter(py.or2(py.get(g, "tasks", []), () => ([])))]);
  var graph_storage: any = new SemanticGraphStorage();
  var node: any;
  for (node of py.iter(topology_nodes)) {
    if ((((node !== null && typeof node === "object" && !Array.isArray(node) && !(node instanceof Set) && !(node instanceof Map))) && py.truthy(py.get(node, "id")))) {
      graph_storage.add_node(node);
    }
  }
  var edge: any;
  for (edge of py.iter(py.get(bytecode_ir, "edges", []))) {
    if (((edge !== null && typeof edge === "object" && !Array.isArray(edge) && !(edge instanceof Set) && !(edge instanceof Map)))) {
      graph_storage.add_edge(edge);
    }
  }
  var graph_snapshot: any = graph_storage.snapshot();
  var topo_nodes: any = py.get(distributed_topology, "nodes", []);
  var member_ids: any = py.sorted(py.iter(topo_nodes).filter((n: any) => (((n !== null && typeof n === "object" && !Array.isArray(n) && !(n instanceof Set) && !(n instanceof Map))) && py.truthy(py.get(n, "id")))).map((n: any) => py.get(n, "id")));
  var hypergraph_rels: any[] = [];
  if ((py.len(member_ids) >= 2)) {
    py.listAppend(hypergraph_rels, {"type": "runtime_cluster", "members": member_ids});
  }
  var hypergraph: any = buildSemanticHypergraph(topo_nodes, hypergraph_rels);
  var graph_db: any = new SemanticGraphDatabase();
  for (node of py.iter(topo_nodes)) {
    if (((node !== null && typeof node === "object" && !Array.isArray(node) && !(node instanceof Set) && !(node instanceof Map)))) {
      graph_db.insert_node(node);
    }
  }
  for (edge of py.iter(py.get(distributed_topology, "edges", []))) {
    if (((edge !== null && typeof edge === "object" && !Array.isArray(edge) && !(edge instanceof Set) && !(edge instanceof Map)))) {
      graph_db.insert_edge(edge);
    }
  }
  var graph_db_stats: any = graph_db.stats();
  var wal: any = new SemanticWAL();
  py.listAppend(wal, {"event": "runtime_compiled"});
  var wal_state: any = wal.replay();
  var worker_assignments: any = assignDistributedWorkers([...py.iter(py.or2(py.get(g, "tasks", []), () => ([])))]);
  var execution_plan: any = compileExecutionPlan(bytecode_ir);
  var routing: any = routeSemanticTasks([...py.iter(py.or2(py.get(g, "tasks", []), () => ([])))], py.or2(topo_nodes, () => (topology_nodes)));
  var runtime_snapshot: any = createRuntimeSnapshot({"vm": vm_result, "journal": journal_state});
  var runtime_consistency: any = proveSemanticRuntimeConsistency(vm_result);
  var actor_system: any = new SemanticActorSystem();
  actor_system.create_actor("runtime");
  actor_system.send("runtime", {"event": "boot"});
  var actor_message: any = actor_system.receive("runtime");
  var memory_fabric: any = new SemanticMemoryFabric();
  memory_fabric.put("runtime", "snapshot", runtime_snapshot);
  var memory_value: any = py.get(memory_fabric, "runtime", "snapshot");
  var consensus: any = computeSemanticConsensus([{"value": "stable"}, {"value": "stable"}]);
  var stream: any = new SemanticStream();
  stream.push({"event": "runtime_start"});
  var stream_event: any = stream.next();
  var filesystem: any = new SemanticFilesystem();
  filesystem.write("/runtime/state", "active");
  var replication: any = replicateSemanticRegion(runtime_snapshot, 3);
  var transaction_coordination: any = coordinateTransactions([{"id": "tx1"}]);
  var cluster_state: any = computeClusterState(py.get(distributed_topology, "nodes", []));
  var distributed_cache: any = new DistributedSemanticCache();
  var distributed_cache_key: any = distributed_cache.put(runtime_snapshot);
  var cached_snapshot: any = py.get(distributed_cache, distributed_cache_key);
  var crdt_state: any = mergeSemanticStates({"a": 1}, {"a": 2});
  var compiler_pipeline: any = compileSemanticPipeline(bytecode_ir);
  var schedule_nodes: any = py.or2(py.sorted(py.iter(topo_nodes).filter((n: any) => (((n !== null && typeof n === "object" && !Array.isArray(n) && !(n instanceof Set) && !(n instanceof Map))) && py.truthy(py.get(n, "id")))).map((n: any) => py.toStr(py.get(n, "id")))), () => (["node_a", "node_b"]));
  var distributed_schedule: any = scheduleDistributedExecution(py.get(py.get(compiler_pipeline, "execution_plan", {}), "plan", []), schedule_nodes);
  var distributed_checkpoint: any = createDistributedCheckpoint(compiler_pipeline);
  var semantic_query: any = executeSemanticQuery(py.get(distributed_topology, "nodes", []), {});
  var parsed_query: any = parseSemanticQuery("SELECT id WHERE type = service LIMIT 10");
  var query_ast: any = buildQueryAst(parsed_query);
  var semantic_query_plan: any = planSemanticQuery(query_ast);
  var optimized_query_plan: any = optimizeSemanticQuery(semantic_query_plan);
  var query_execution: any = executeSemanticPlan(optimized_query_plan, py.get(distributed_topology, "nodes", []));
  var dag_execution: any = executeSemanticDag(py.get(distributed_topology, "nodes", []));
  var resource_accounting: any = accountSemanticResources(optimized_semantic_ir);
  var execution_coordination: any = coordinateDistributedExecution([distributed_schedule]);
  var agent_runtime: any = new SemanticAgentRuntime();
  var runtime_agent: any = new SemanticAgent("runtime", ["execute"]);
  agent_runtime.register(runtime_agent);
  var boot_payload: any = {"task": "boot"};
  var boundary: any = validateSemanticBoundary(boot_payload);
  var agent_result: any = (py.truthy(py.get(boundary, "accepted")) ? agent_runtime.execute("runtime", boot_payload) : {"status": "blocked", "agent_id": "runtime"});
  var task_graph: any = buildSemanticTaskGraph([...py.iter(py.or2(py.get(g, "tasks", []), () => ([])))]);
  var platform_event_bus: any = new SemanticEventBus();
  platform_event_bus.publish({"event": "runtime_boot"});
  var service_mesh: any = buildSemanticServiceMesh(py.get(distributed_topology, "nodes", []));
  var semantic_cluster: any = orchestrateSemanticCluster(py.get(distributed_topology, "nodes", []));
  var platform_resource_schedule: any = scheduleSemanticResources([...py.iter(py.or2(py.get(g, "tasks", []), () => ([])))]);
  var runtime_policy: any = enforceRuntimePolicy({"compiler": true, "query": true});
  var repository_irs: any = [...py.iter(py.or2(py.get(g, "repository_irs", []), () => ([])))];
  if ((!py.truthy(repository_irs) && py.truthy(path))) {
    repository_irs = [{"path": path, "semantic_ast": semantic_ir}];
  }
  var repository_world_model: any = buildRepositoryWorldModel(repository_irs);
  var architecture_graph: any = buildSemanticArchitectureGraph(repository_irs);
  var impact_analysis: any = analyzeSemanticImpact(path, architecture_graph);
  var semantic_autonomy: any = orchestrateSemanticRuntime({"goal": py.or2(path, () => ("compile_runtime"))});
  var evolution_context: any = py.pyDict(semantic_autonomy);
  py.setItem(evolution_context, "architecture_graph", architecture_graph);
  py.setItem(evolution_context, "repository_world_model", repository_world_model);
  var semantic_evolution: any = orchestrateSemanticEvolution(evolution_context);
  var engineering_context: any = py.pyDict(semantic_evolution);
  py.setItem(engineering_context, "distributed_topology", distributed_topology);
  py.setItem(engineering_context, "transitions", [...py.iter(py.or2(py.get(g, "transitions", []), () => ([])))]);
  py.setItem(engineering_context, "graph_database", graph_db_stats);
  py.setItem(engineering_context, "events", events);
  py.setItem(engineering_context, "repository_world_model", repository_world_model);
  var semantic_engineering: any = orchestrateSemanticEngineering(engineering_context);
  var execution_reality_context: any = {"distributed_topology": distributed_topology, "transitions": transitions, "event_stream": event_stream, "semantic_crdt": crdt_state, "tasks": [...py.iter(py.or2(py.get(g, "tasks", []), () => ([])))], "distributed_workers": py.get(worker_assignments, "assignments", []), "journal": journal_state};
  var semantic_execution_reality: any = orchestrateExecutionReality(execution_reality_context);
  var causal_intelligence_context: any = {"distributed_topology": distributed_topology, "transitions": transitions, "event_stream": event_stream, "runtime_entropy": py.get(semantic_execution_reality, "runtime_entropy", {}), "execution_pressure": py.get(semantic_execution_reality, "execution_pressure", {}), "runtime_conflicts": py.get(semantic_execution_reality, "runtime_conflicts", {}), "journal": journal_state, "tasks": [...py.iter(py.or2(py.get(g, "tasks", []), () => ([])))], "distributed_workers": py.get(worker_assignments, "assignments", [])};
  var semantic_causal_intelligence: any = orchestrateSemanticCausalIntelligence(causal_intelligence_context);
  var execution_physics_context: any = {"distributed_topology": distributed_topology, "transitions": transitions, "events": [...py.iter((((event_stream !== null && typeof event_stream === "object" && !Array.isArray(event_stream) && !(event_stream instanceof Set) && !(event_stream instanceof Map))) ? py.get(event_stream, "events", []) : []))], "distributed_workers": py.get(worker_assignments, "assignments", []), "runtime_entropy": py.get(semantic_execution_reality, "runtime_entropy", {}), "journal": journal_state, "tasks": [...py.iter(py.or2(py.get(g, "tasks", []), () => ([])))], "runtime_conflicts": py.get(semantic_execution_reality, "runtime_conflicts", {}), "state_convergence": py.get(semantic_causal_intelligence, "runtime_equilibrium", {})};
  var semantic_execution_physics: any = orchestrateExecutionPhysics(execution_physics_context);
  return {"execution": execution, "topology": topology, "ssa": ssa, "multilang_ssa": multilang_ssa, "tree_sitter": {"available": py.get(tree_sitter, "available", false), "language": lang, "reason": py.get(tree_sitter, "reason")}, "event_stream": event_stream, "distributed_topology": distributed_topology, "distributed_partitions": distributed_partitions, "universal_ast": universal_ast, "semantic_ir": semantic_ir, "optimized_semantic_ir": optimized_semantic_ir, "runtime_simulation": runtime_simulation, "semantic_replay": semantic_replay, "execution_reconciliation": execution_reconciliation, "topology_convergence": topology_convergence, "execution_optimizer": execution_optimizer, "query_plan": query_plan, "cache_key": cache_key, "persistence": persistence, "semantic_bytecode": bytecode, "semantic_vm": vm_result, "transaction": transaction_result, "journal": journal_state, "dependency_resolution": dependency_resolution, "graph_storage": graph_snapshot, "semantic_hypergraph": hypergraph, "graph_database": graph_db_stats, "semantic_wal": wal_state, "distributed_workers": worker_assignments, "execution_plan": execution_plan, "distributed_routing": routing, "runtime_snapshot_v2": runtime_snapshot, "runtime_consistency": runtime_consistency, "semantic_actor_message": actor_message, "semantic_memory_fabric": memory_value, "semantic_consensus": consensus, "semantic_stream_event": stream_event, "semantic_filesystem": filesystem.list_paths(), "semantic_replication": replication, "transaction_coordination": transaction_coordination, "cluster_state": cluster_state, "distributed_cache_key": distributed_cache_key, "distributed_cached_snapshot": cached_snapshot, "semantic_crdt": crdt_state, "compiler_pipeline": compiler_pipeline, "distributed_schedule": distributed_schedule, "distributed_checkpoint": distributed_checkpoint, "semantic_query": semantic_query, "query_ast": query_ast, "query_plan_v2": optimized_query_plan, "query_execution": query_execution, "dag_execution": dag_execution, "resource_accounting": resource_accounting, "execution_coordination": execution_coordination, "semantic_agent": agent_result, "semantic_task_graph": task_graph, "semantic_service_mesh": service_mesh, "semantic_cluster": semantic_cluster, "platform_resource_schedule": platform_resource_schedule, "runtime_policy": runtime_policy, "security_boundary": boundary, "repository_world_model": repository_world_model, "semantic_architecture_graph": architecture_graph, "semantic_impact_analysis": impact_analysis, "semantic_autonomy": semantic_autonomy, "semantic_evolution": semantic_evolution, "semantic_engineering": semantic_engineering, "semantic_execution_reality": semantic_execution_reality, "semantic_causal_intelligence": semantic_causal_intelligence, "semantic_execution_physics": semantic_execution_physics, "bounded": true, "deterministic": true};
}
export { DistributedSemanticCache, SemanticActorSystem, SemanticAgent, SemanticAgentRuntime, SemanticCache, SemanticEventBus, SemanticFilesystem, SemanticGraphDatabase, SemanticGraphStorage, SemanticJournal, SemanticMemoryFabric, SemanticStream, SemanticTransaction, SemanticVirtualMachine, SemanticWAL, accountSemanticResources, analyzeSemanticImpact, assignDistributedWorkers, buildDistributedTopology, buildMultilangSsa, buildQueryAst, buildQueryPlan, buildRepositoryWorldModel, buildSemanticArchitectureGraph, buildSemanticHypergraph, buildSemanticServiceMesh, buildSemanticTaskGraph, buildSsaForm, compileExecutionIr, compileExecutionPlan, compileSemanticBytecode, compileSemanticPipeline, compileTopologyIr, computeClusterState, computeSemanticConsensus, convergeRuntimeAndTopology, coordinateDistributedExecution, coordinateTransactions, createDistributedCheckpoint, createParser, createRuntimeSnapshot, detectLanguage, enforceRuntimePolicy, executeSemanticDag, executeSemanticPlan, executeSemanticQuery, mergeSemanticStates, optimizeExecutionOrder, optimizeSemanticIr, optimizeSemanticQuery, orchestrateExecutionPhysics, orchestrateExecutionReality, orchestrateSemanticCausalIntelligence, orchestrateSemanticCluster, orchestrateSemanticEngineering, orchestrateSemanticEvolution, orchestrateSemanticRuntime, parseSemanticQuery, parseUniversalAst, partitionRuntimeGraph, persistSemanticIr, planSemanticQuery, proveSemanticRuntimeConsistency, reconcileExecutionGraphs, reconstructEventStream, replaySemanticEvents, replicateSemanticRegion, resolveDependencies, routeSemanticTasks, scheduleDistributedExecution, scheduleSemanticResources, simulateRuntimeExecution, validateSemanticBoundary };
