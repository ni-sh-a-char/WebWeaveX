/**
 * Converted from Python: core/synchronization/runtime_sync_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileSynchronizationRuntimeIr, synchronizationRuntimeIrToGraph } from "../ir/synchronizationRuntimeIr.js";
import { replicateRuntimeReality } from "./realityReplicationEngine.js";
import { alignRuntimeLayers } from "./runtimeAlignmentEngine.js";
import { maintainRuntimeContinuity } from "./runtimeContinuityEngine.js";
import { convergeRuntimeState } from "./runtimeConvergenceEngine.js";
import { buildRuntimeDelta } from "./runtimeDeltaEngine.js";
import { diffRuntimeState } from "./runtimeDiffEngine.js";
import { detectRuntimeDrift } from "./runtimeDriftEngine.js";
import { federateRuntimeRealities } from "./runtimeFederationEngine.js";
import { buildRuntimeHistory } from "./runtimeHistoryEngine.js";
import { mergeRuntimeRealities } from "./runtimeMergeEngine.js";
import { trackRuntimeMutations } from "./runtimeMutationEngine.js";
import { replaySynchronizedRuntime } from "./runtimeReplayEngine.js";
import { captureRuntimeSnapshot } from "./runtimeSnapshotEngine.js";
import { buildRuntimeStateGraph } from "./runtimeStateGraphEngine.js";
import { synchronizeRuntime } from "./runtimeSyncEngine.js";
import { loadSyncMemory } from "./runtimeSyncMemoryEngine.js";
import { rememberSyncRuntime } from "./runtimeSyncMemoryEngine.js";
import { saveSyncMemory } from "./runtimeSyncMemoryEngine.js";
import { verifyRuntimeConsistency } from "./runtimeConsistencyEngine.js";
import { buildSyncTimeline } from "./runtimeTimelineEngine.js";
import { buildRuntimeGraph } from "../runtime_graph/runtimeGraphEngine.js";

export function _runtimeView(extraction: any = null, semantic: any = null, workflow: any = null, causality: any = null): any {
  return {"dom": py.get(py.or2(extraction, () => ({})), "dom", {}), "semantic": py.get(py.or2(semantic, () => ({})), "semantic", py.or2(semantic, () => ({}))), "workflow": py.get(py.or2(workflow, () => ({})), "workflow", py.or2(workflow, () => ({}))), "causality": py.get(py.or2(causality, () => ({})), "causality", py.or2(causality, () => ({}))), "runtime": py.get(py.or2(extraction, () => ({})), "runtime", {})};
}
export function runSynchronizedRuntime(tick: any = 0, browser: any = null, native: any = null, semantic_result: any = null, workflow_result: any = null, causality_result: any = null, distributed_result: any = null, session: any = null, identity: any = null, memory: any = null, workers: any = null): any {
  memory = py.pyDict(py.or2(memory, () => ({})));
  workers = [...py.iter(py.or2(workers, () => (py.get(py.or2(distributed_result, () => ({})), "workers", []))))];
  var previous_view: any = py.get(memory, "last_view", {});
  var current_view: any = _runtimeView(browser, semantic_result, workflow_result, causality_result);
  var delta: any = buildRuntimeDelta(previous_view, current_view, tick);
  var snapshot: any = captureRuntimeSnapshot(browser, native, semantic_result, workflow_result, causality_result, py.get(memory, "continuity", {}), tick);
  var drift: any = detectRuntimeDrift({"selectors": py.get(previous_view, "dom", {}), "semantic": py.get(previous_view, "semantic", {}), "workflow": py.get(previous_view, "workflow", {}), "topology": py.get(previous_view, "runtime", {}), "application": py.get(previous_view, "workflow", {}), "runtime": py.get(previous_view, "runtime", {})}, {"selectors": py.get(current_view, "dom", {}), "semantic": py.get(current_view, "semantic", {}), "workflow": py.get(current_view, "workflow", {}), "topology": py.get(current_view, "runtime", {}), "application": py.get(current_view, "workflow", {}), "runtime": py.get(current_view, "runtime", {})});
  var state_diff: any = diffRuntimeState(previous_view, current_view);
  var mutations: any = py.callKw(trackRuntimeMutations as (...a: any[]) => any, ["prior", "mutation"], {"prior": py.get(delta, "changes", []), "tick": tick});
  var realities: any = [{"reality_id": "primary", "tick": tick, "semantic": py.get(current_view, "semantic", {}), "workflow": py.get(current_view, "workflow", {}), "application": py.get(current_view, "workflow", {})}];
  if (py.truthy(distributed_result)) {
    py.listAppend(realities, {"reality_id": "distributed", "tick": tick, "semantic": {}, "workflow": distributed_result, "application": {}});
  }
  var merged: any = mergeRuntimeRealities(realities);
  var convergence: any = convergeRuntimeState(realities);
  var synchronization: any = synchronizeRuntime([snapshot], tick);
  var replication: any = replicateRuntimeReality({"reality_id": "primary", "semantic_state": py.get(current_view, "semantic", {}), "runtime_state": py.get(current_view, "runtime", {}), "workflows": py.get(current_view, "workflow", {}), "checkpoints": py.get(memory, "checkpoints", []), "causality_graph": py.get(current_view, "causality", {})}, workers);
  var federation: any = federateRuntimeRealities(workers, browser, native, semantic_result, workflow_result);
  var alignment: any = alignRuntimeLayers(browser, native, semantic_result, workflow_result);
  var continuity: any = maintainRuntimeContinuity(session, identity, workflow_result, semantic_result, py.get(memory, "checkpoint", {}));
  var prior_deltas: any = [...py.iter(py.get(memory, "deltas", []))];
  var all_deltas: any = py.add(prior_deltas, [delta]);
  var history: any = buildRuntimeHistory(all_deltas, undefined, [py.get(merged, "workflow", {})]);
  var timeline: any = buildSyncTimeline(history);
  var state_graph: any = buildRuntimeStateGraph(snapshot, delta, convergence);
  var payload: any = {"snapshot": snapshot, "delta": delta, "drift": drift, "diff": state_diff, "mutations": mutations, "merge": merged, "convergence": convergence, "synchronization": synchronization, "replication": replication, "federation": federation, "alignment": alignment, "continuity": continuity, "history": history, "timeline": timeline, "state_graph": state_graph, "bounded": true};
  var updated_memory: any = rememberSyncRuntime(memory, {"deltas": all_deltas, "history": history, "timeline": timeline, "convergence": convergence, "realities": realities, "continuity": continuity, "state_graph": state_graph, "last_view": current_view});
  var replay: any = replaySynchronizedRuntime(updated_memory);
  var consistency: any = verifyRuntimeConsistency(history, convergence, replay);
  py.setItem(payload, "memory", updated_memory);
  py.setItem(payload, "replay", replay);
  py.setItem(payload, "consistency", consistency);
  py.setItem(payload, "sync_ir", compileSynchronizationRuntimeIr(payload));
  return payload;
}
export function runSyncForExtraction(synchronized_runtime: any = true, memory_path: any = "", memory_key: any = "", tick: any = 0, browser: any = null, native: any = null, semantic_result: any = null, workflow_result: any = null, causality_result: any = null, distributed_result: any = null, session: any = null, identity: any = null, merge_graph: any = true): any {
  if (!py.truthy(synchronized_runtime)) {
    return {"enabled": false, "bounded": true};
  }
  var memory: Record<string, any> = {};
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    var loaded: any = loadSyncMemory(memory_path, memory_key);
    if (py.truthy(py.get(loaded, "available"))) {
      memory = py.get(loaded, "memory", memory);
    }
  }
  var result: any = runSynchronizedRuntime(tick, browser, native, semantic_result, workflow_result, causality_result, distributed_result, session, identity, memory);
  var persisted: any = false;
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    saveSyncMemory(memory_path, py.get(result, "memory", {}), memory_key);
    persisted = true;
  }
  var graph_ir: any = synchronizationRuntimeIrToGraph(py.get(result, "sync_ir", {}));
  var unified_graph: Record<string, any> = {};
  if (py.truthy(merge_graph)) {
    unified_graph = buildRuntimeGraph([graph_ir]);
  }
  return {"enabled": true, "synchronization": result, "sync_ir": py.get(result, "sync_ir", {}), "sync_graph_ir": graph_ir, "unified_graph": unified_graph, "replay": py.get(result, "replay", {}), "memory_persisted": persisted, "bounded": true};
}
export { alignRuntimeLayers, buildRuntimeDelta, buildRuntimeGraph, buildRuntimeHistory, buildRuntimeStateGraph, buildSyncTimeline, captureRuntimeSnapshot, compileSynchronizationRuntimeIr, convergeRuntimeState, detectRuntimeDrift, diffRuntimeState, federateRuntimeRealities, loadSyncMemory, maintainRuntimeContinuity, mergeRuntimeRealities, rememberSyncRuntime, replaySynchronizedRuntime, replicateRuntimeReality, saveSyncMemory, synchronizationRuntimeIrToGraph, synchronizeRuntime, trackRuntimeMutations, verifyRuntimeConsistency };
