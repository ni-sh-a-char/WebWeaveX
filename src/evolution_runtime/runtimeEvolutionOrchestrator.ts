/**
 * Converted from Python: core/evolution_runtime/runtime_evolution_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { adaptRuntimeStrategy } from "./runtimeAdaptationEngine.js";
import { convergeRuntimeEvolution } from "./runtimeConvergenceEngine.js";
import { diffEvolutionRuntime } from "./runtimeDiffEngine.js";
import { buildRuntimeEvolution } from "./runtimeEvolutionEngine.js";
import { buildRuntimeEvolutionGraph } from "./runtimeEvolutionGraphEngine.js";
import { buildRuntimeLineage } from "./runtimeLineageEngine.js";
import { loadEvolutionRuntime } from "./runtimeMemoryEngine.js";
import { rememberEvolutionRuntime } from "./runtimeMemoryEngine.js";
import { saveEvolutionRuntime } from "./runtimeMemoryEngine.js";
import { buildRuntimeMutations } from "./runtimeMutationEngine.js";
import { optimizeRuntimeExecution } from "./runtimeOptimizationEngine.js";
import { buildRuntimePatterns } from "./runtimePatternEngine.js";
import { buildRuntimePolicy } from "./runtimePolicyEngine.js";
import { enforceRuntimePolicy } from "./runtimePolicyEngine.js";
import { evolveRecoveryOrder } from "./runtimeRecoveryEvolutionEngine.js";
import { repairRuntimeFailures } from "./runtimeRepairEngine.js";
import { buildRuntimeStrategy } from "./runtimeStrategyEngine.js";
import { evolveSelectorRuntime } from "./selectorEvolutionEngine.js";
import { evolveSemanticRuntime } from "./semanticEvolutionEngine.js";
import { evolveRuntimeTopology } from "./topologyEvolutionEngine.js";
import { evolveWorkflowRuntime } from "./workflowEvolutionEngine.js";
import { compileEvolutionRuntimeIr, evolutionRuntimeIrToGraph } from "../ir/evolutionRuntimeIr.js";
import { buildRuntimeGraph } from "../runtime_graph/runtimeGraphEngine.js";

export function runEvolutionRuntime(adaptive_memory: any = null, workflow_result: any = null, semantic_result: any = null, sync_result: any = null, distributed_result: any = null, failures: any = null, memory: any = null, tick: any = 0): any {
  memory = py.pyDict(py.or2(memory, () => ({})));
  adaptive_memory = py.or2(adaptive_memory, () => ({}));
  failures = py.or2(failures, () => ([]));
  var healed: any = py.pyDict(py.get(adaptive_memory, "healed_selectors", {}));
  var selector: any = evolveSelectorRuntime(py.get(adaptive_memory, "selectors", {}), healed);
  var workflow_inner: any = py.get(py.or2(workflow_result, () => ({})), "workflow", py.or2(workflow_result, () => ({})));
  var workflow: any = evolveWorkflowRuntime(py.get(workflow_inner, "plan", {}), py.get(workflow_inner, "execution", {}), py.get(memory, "evolution_histories", []));
  var semantic: any = evolveSemanticRuntime(semantic_result, py.get(memory, "evolution_histories", []));
  var sync_inner: any = py.get(py.or2(sync_result, () => ({})), "synchronization", py.or2(sync_result, () => ({})));
  var topology: any = evolveRuntimeTopology(py.get(py.or2(distributed_result, () => ({})), "workers", []), sync_inner, py.get(py.or2(sync_result, () => ({})), "causality"));
  var evidence: any = {"drift_count": py.len(py.get(py.get(sync_inner, "drift", {}), "drifts", [])), "failed_steps": py.count(failures, "failed_workflow")};
  var strategy: any = buildRuntimeStrategy(evidence);
  var repairs: any = repairRuntimeFailures(failures, healed);
  var recovery: any = evolveRecoveryOrder(py.get(repairs, "repairs", []));
  var depth: any = py.len(py.get(workflow, "execution_ordering", []));
  var optimization: any = optimizeRuntimeExecution(depth, py.len(py.get(memory, "evolution_histories", [])), py.len(py.get(sync_inner, "deltas", [])));
  var adapted_strategy: any = adaptRuntimeStrategy(strategy, optimization);
  var mutations: any = buildRuntimeMutations(selector, workflow, semantic, py.get(sync_inner, "convergence", {}));
  var parent_id: any = py.toStr(py.get(memory, "last_evolution_id", ""));
  var lineage: any = buildRuntimeLineage("", mutations, parent_id);
  var evolution: any = buildRuntimeEvolution(mutations, lineage);
  py.setItem(evolution, "evolution_id", py.at(evolution, "evolution_id"));
  lineage = buildRuntimeLineage(py.at(evolution, "evolution_id"), mutations, parent_id);
  var policy: any = buildRuntimePolicy();
  var enforcement: any = enforceRuntimePolicy(policy, mutations, py.get(repairs, "repairs", []), depth);
  var patterns: any = buildRuntimePatterns(py.get(py.get(py.or2(semantic_result, () => ({})), "semantic", {}), "ui", {}), [py.get(workflow_inner, "plan", {})], semantic_result, py.get(memory, "evolution_histories", []));
  var graph: any = buildRuntimeEvolutionGraph(evolution, repairs, optimization);
  var prior: any = py.get(memory, "last_evolution", {});
  var diff: any = (py.truthy(prior) ? diffEvolutionRuntime(prior, evolution) : {"revertible": true});
  var distributed_evolutions: any = [evolution];
  if (py.truthy(py.get(memory, "distributed_evolutions"))) {
    py.extend(distributed_evolutions, py.at(memory, "distributed_evolutions"));
  }
  var convergence: any = convergeRuntimeEvolution(distributed_evolutions);
  var payload: any = {"evolution": evolution, "selector": selector, "workflow": workflow, "semantic": semantic, "topology": topology, "strategy": adapted_strategy, "repairs": repairs, "recovery": recovery, "optimization": optimization, "patterns": patterns, "lineage": lineage, "graph": graph, "policy": policy, "enforcement": enforcement, "convergence": convergence, "diff": diff, "tick": tick, "bounded": true};
  var updated_memory: any = rememberEvolutionRuntime(memory, {"evolution_histories": py.add([...py.iter(py.get(memory, "evolution_histories", []))], [evolution]), "selector_lineage": lineage, "workflow_evolution": workflow, "semantic_evolution": semantic, "optimization_histories": py.add([...py.iter(py.get(memory, "optimization_histories", []))], [optimization]), "last_evolution": evolution, "last_evolution_id": py.at(evolution, "evolution_id"), "distributed_evolutions": py.slice(distributed_evolutions, (-10), null)});
  py.setItem(payload, "memory", updated_memory);
  py.setItem(payload, "replay", {"lineage": lineage, "evolution": evolution, "replayed": true, "bounded": true});
  py.setItem(payload, "evolution_ir", compileEvolutionRuntimeIr(payload));
  return payload;
}
export function runEvolutionForExtraction(evolving_runtime: any = true, memory_path: any = "", memory_key: any = "", adaptive_memory: any = null, workflow_result: any = null, semantic_result: any = null, sync_result: any = null, distributed_result: any = null, failures: any = null, tick: any = 0, merge_graph: any = true): any {
  if (!py.truthy(evolving_runtime)) {
    return {"enabled": false, "bounded": true};
  }
  var memory: Record<string, any> = {};
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    var loaded: any = loadEvolutionRuntime(memory_path, memory_key);
    if (py.truthy(py.get(loaded, "available"))) {
      memory = py.get(loaded, "memory", memory);
    }
  }
  var result: any = runEvolutionRuntime(adaptive_memory, workflow_result, semantic_result, sync_result, distributed_result, failures, memory, tick);
  var persisted: any = false;
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    saveEvolutionRuntime(memory_path, py.get(result, "memory", {}), memory_key);
    persisted = true;
  }
  var graph_ir: any = evolutionRuntimeIrToGraph(py.get(result, "evolution_ir", {}));
  var unified_graph: Record<string, any> = {};
  if (py.truthy(merge_graph)) {
    unified_graph = buildRuntimeGraph([graph_ir]);
  }
  return {"enabled": true, "evolution": result, "evolution_ir": py.get(result, "evolution_ir", {}), "evolution_graph_ir": graph_ir, "unified_graph": unified_graph, "replay": py.get(result, "replay", {}), "memory_persisted": persisted, "bounded": true};
}
export { adaptRuntimeStrategy, buildRuntimeEvolution, buildRuntimeEvolutionGraph, buildRuntimeGraph, buildRuntimeLineage, buildRuntimeMutations, buildRuntimePatterns, buildRuntimePolicy, buildRuntimeStrategy, compileEvolutionRuntimeIr, convergeRuntimeEvolution, diffEvolutionRuntime, enforceRuntimePolicy, evolutionRuntimeIrToGraph, evolveRecoveryOrder, evolveRuntimeTopology, evolveSelectorRuntime, evolveSemanticRuntime, evolveWorkflowRuntime, loadEvolutionRuntime, optimizeRuntimeExecution, rememberEvolutionRuntime, repairRuntimeFailures, saveEvolutionRuntime };
