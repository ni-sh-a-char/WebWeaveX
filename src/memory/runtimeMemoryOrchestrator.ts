/**
 * Converted from Python: core/memory/runtime_memory_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileRuntimeMemoryIr, runtimeMemoryIrToGraph } from "../ir/runtimeMemoryIr.js";
import { buildDistributedMemory } from "./distributedMemoryEngine.js";
import { buildKnowledgeMemory } from "./knowledgeMemoryEngine.js";
import { convergeRuntimeMemory } from "./runtimeConvergenceMemoryEngine.js";
import { diffRuntimeMemory } from "./runtimeDiffMemoryEngine.js";
import { federateRuntimeMemory } from "./runtimeFederationEngine.js";
import { buildRuntimeMemoryGraph } from "./runtimeGraphMemoryEngine.js";
import { appendRuntimeHistory } from "./runtimeHistoryEngine.js";
import { buildRuntimeIndex } from "./runtimeIndexEngine.js";
import { buildRuntimeLineageMemory } from "./runtimeLineageMemoryEngine.js";
import { buildRuntimeMemory } from "./runtimeMemoryEngine.js";
import { loadRuntimeMemory } from "./runtimeMemoryPersistenceEngine.js";
import { saveRuntimeMemory } from "./runtimeMemoryPersistenceEngine.js";
import { buildRuntimeMemoryPolicy } from "./runtimeMemoryPolicyEngine.js";
import { enforceMemoryPolicy } from "./runtimeMemoryPolicyEngine.js";
import { mergeRuntimeMemories } from "./runtimeMergeEngine.js";
import { queryRuntimeMemory } from "./runtimeQueryEngine.js";
import { replicateRuntimeMemory } from "./runtimeReplicationEngine.js";
import { searchRuntimeMemory } from "./runtimeSearchEngine.js";
import { captureMemorySnapshot } from "./runtimeSnapshotMemoryEngine.js";
import { buildSemanticMemory } from "./semanticMemoryEngine.js";
import { buildRuntimeGraph } from "../runtime_graph/runtimeGraphEngine.js";

export function _collectHistory(sources: any, tick: any): any {
  var history: any[] = [];
  if (py.truthy(py.get(sources, "workflow"))) {
    py.listAppend(history, {"tick": tick, "kind": "workflow", "source": "workflow"});
  }
  if (py.truthy(py.get(sources, "sync"))) {
    py.listAppend(history, {"tick": tick, "kind": "sync", "source": "sync"});
  }
  if (py.truthy(py.get(sources, "evolution"))) {
    py.listAppend(history, {"tick": tick, "kind": "evolution", "source": "evolution"});
  }
  if (py.truthy(py.get(sources, "live"))) {
    py.listAppend(history, {"tick": tick, "kind": "live", "source": "connectors"});
  }
  if (py.truthy(py.get(sources, "extraction"))) {
    py.listAppend(history, {"tick": tick, "kind": "extraction", "source": "browser"});
  }
  return history;
}
export function runRuntimeMemory(sources: any = null, stored: any = null, nodes: any = null, tick: any = 0): any {
  sources = py.or2(sources, () => ({}));
  stored = py.pyDict(py.or2(stored, () => ({})));
  nodes = [...py.iter(py.or2(nodes, () => ([{"node_id": "primary", "synced": true}])))];
  var prior_runtime: any = py.get(stored, "runtime", {});
  var history: any = [...py.iter(py.get(prior_runtime, "runtime_history", []))];
  var entry: any;
  for (entry of py.iter(_collectHistory(sources, tick))) {
    history = appendRuntimeHistory(history, entry);
  }
  var entities: any[] = [];
  var relations: any[] = [];
  var semantic_src: any = py.get(sources, "semantic", {});
  if (py.truthy(semantic_src)) {
    var inner: any = py.get(semantic_src, "semantic", semantic_src);
    entities = py.get(py.get(inner, "entities", {}), "entities", []);
    relations = py.get(py.get(inner, "entities", {}), "relations", []);
  }
  var knowledge: any = buildKnowledgeMemory(entities, relations, {"graphs": [py.get(sources, "graph", {})], "distributed": py.get(sources, "distributed", {}), "application": py.get(sources, "application", {})});
  var semantic: any = buildSemanticMemory(semantic_src, history);
  var lineage: any = buildRuntimeLineageMemory(py.get(py.get(py.get(sources, "evolution", {}), "selector", {}), "selectors", []), [{"id": "wf:0", "ancestor": ""}], py.get(py.get(sources, "sync", {}), "lineage", []), py.get(py.get(sources, "evolution", {}), "lineage", []), [{"id": `extract:${py.toStr(tick)}`, "ancestor": ""}]);
  var runtime: any = buildRuntimeMemory(history, py.get(lineage, "lineage", []), py.get(knowledge, "semantic_relations", []));
  var graph: any = buildRuntimeMemoryGraph(py.get(knowledge, "entities", []), py.get(knowledge, "semantic_relations", []));
  var index: any = buildRuntimeIndex(py.get(knowledge, "entities", []), [{"id": py.get(py.get(sources, "workflow", {}), "objective", "operate")}], [graph], [...py.iter(py.get(py.or2(py.get(py.or2(py.get(sources, "live"), () => ({})), "streams"), () => ({})), "streams", []))], [py.or2(py.get(sources, "live"), () => ({}))]);
  var replication: any = replicateRuntimeMemory(runtime, nodes);
  var convergence: any = convergeRuntimeMemory(py.get(replication, "replicas", []));
  var distributed: any = buildDistributedMemory(nodes);
  var federated: any = federateRuntimeMemory((py.truthy(prior_runtime) ? [runtime, prior_runtime] : [runtime]));
  var merged: any = mergeRuntimeMemories((py.truthy(prior_runtime) ? [runtime, prior_runtime] : [runtime]));
  var policy: any = buildRuntimeMemoryPolicy();
  var enforcement: any = enforceMemoryPolicy(policy, py.get(runtime, "runtime_history", []), py.get(runtime, "lineage", []), py.get(replication, "replica_count", 0));
  var diff: any = (py.truthy(prior_runtime) ? diffRuntimeMemory(prior_runtime, runtime) : {"revertible": true});
  var snapshot: any = captureMemorySnapshot({"runtime": runtime, "knowledge": knowledge, "graph": graph}, tick);
  var payload: any = {"runtime": runtime, "knowledge": knowledge, "semantic": semantic, "lineage": lineage, "graph": graph, "index": index, "distributed": distributed, "federation": federated, "merged": merged, "replication": replication, "convergence": convergence, "policy": policy, "enforcement": enforcement, "diff": diff, "snapshot": snapshot, "bounded": true};
  py.setItem(payload, "replay", {"lineage": py.get(lineage, "lineage", []), "runtime_history": py.get(runtime, "runtime_history", []), "memory_id": py.get(runtime, "memory_id", ""), "replayed": true, "bounded": true});
  py.setItem(payload, "memory_ir", compileRuntimeMemoryIr(payload));
  return payload;
}
export function runMemoryForExtraction(federated_memory: any = true, memory_path: any = "", memory_key: any = "", sources: any = null, nodes: any = null, tick: any = 0, merge_graph: any = true): any {
  if (!py.truthy(federated_memory)) {
    return {"enabled": false, "bounded": true};
  }
  var stored: Record<string, any> = {};
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    var loaded: any = loadRuntimeMemory(memory_path, memory_key);
    if (py.truthy(py.get(loaded, "available"))) {
      stored = py.get(loaded, "memory", stored);
    }
  }
  var result: any = runRuntimeMemory(sources, stored, nodes, tick);
  var store: any = {"runtime": py.get(result, "runtime", {}), "knowledge": py.get(result, "knowledge", {}), "semantic": py.get(result, "semantic", {}), "index": py.get(result, "index", {}), "graph": py.get(result, "graph", {}), "lineage": py.get(result, "lineage", {}), "snapshot": py.get(result, "snapshot", {}), "bounded": true};
  var persisted: any = false;
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    saveRuntimeMemory(memory_path, store, memory_key);
    persisted = true;
  }
  var graph_ir: any = runtimeMemoryIrToGraph(py.get(result, "memory_ir", {}));
  var unified_graph: Record<string, any> = {};
  if (py.truthy(merge_graph)) {
    unified_graph = buildRuntimeGraph([graph_ir]);
  }
  return {"enabled": true, "memory": result, "memory_ir": py.get(result, "memory_ir", {}), "memory_graph_ir": graph_ir, "unified_graph": unified_graph, "replay": py.get(result, "replay", {}), "query": queryRuntimeMemory(py.get(result, "runtime", {}), "semantic", ""), "search": searchRuntimeMemory(py.get(result, "index", {}), ""), "memory_persisted": persisted, "bounded": true};
}
export { appendRuntimeHistory, buildDistributedMemory, buildKnowledgeMemory, buildRuntimeGraph, buildRuntimeIndex, buildRuntimeLineageMemory, buildRuntimeMemory, buildRuntimeMemoryGraph, buildRuntimeMemoryPolicy, buildSemanticMemory, captureMemorySnapshot, compileRuntimeMemoryIr, convergeRuntimeMemory, diffRuntimeMemory, enforceMemoryPolicy, federateRuntimeMemory, loadRuntimeMemory, mergeRuntimeMemories, queryRuntimeMemory, replicateRuntimeMemory, runtimeMemoryIrToGraph, saveRuntimeMemory, searchRuntimeMemory };
