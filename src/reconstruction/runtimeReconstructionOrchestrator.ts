/**
 * Converted from Python: core/reconstruction/runtime_reconstruction_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileReconstructionRuntimeIr, reconstructionRuntimeIrToGraph } from "../ir/reconstructionRuntimeIr.js";
import { reconstructApplicationRuntime } from "./applicationReconstructionEngine.js";
import { reconstructBrowserRuntime } from "./browserReconstructionEngine.js";
import { cloneRuntimeEnvironment } from "./runtimeCloneEngine.js";
import { reconstructConnectorRuntime } from "./runtimeConnectorReconstruction.js";
import { buildRuntimeEnvironment } from "./runtimeEnvironmentEngine.js";
import { fabricateRuntimeReality } from "./runtimeFabricationEngine.js";
import { reconstructRuntimeIdentity } from "./runtimeIdentityReconstruction.js";
import { reconstructRuntimeMemory } from "./runtimeMemoryReconstruction.js";
import { recoverReconstructedRuntime } from "./runtimeRecoveryReconstruction.js";
import { reconstructRuntime } from "./runtimeReconstructionEngine.js";
import { buildRuntimeReplay } from "./runtimeReplayBuilder.js";
import { captureReconstructionSnapshot, loadReconstructionSnapshot, saveReconstructionSnapshot } from "./runtimeSnapshotEngine.js";
import { rebuildRuntimeState } from "./runtimeStateRebuilder.js";
import { buildRuntimeTimeline } from "./runtimeTimelineEngine.js";
import { reconstructRuntimeTopology } from "./runtimeTopologyReconstruction.js";
import { validateReconstructedRuntime } from "./runtimeValidationEngine.js";
import { reconstructRuntimeSession } from "./sessionReconstructionEngine.js";
import { buildRuntimeGraph } from "../runtime_graph/runtimeGraphEngine.js";

export function runReconstructionRuntime(sources: any = null, stored: any = null, runtime_graph: any = null, runtime_type: any = "browser", tick: any = 0, fabricate: any = false, clone: any = false): any {
  sources = py.or2(sources, () => ({}));
  stored = py.pyDict(py.or2(stored, () => ({})));
  runtime_graph = py.or2(runtime_graph, () => (py.get(sources, "graph", {})));
  var semantic_ir: any = py.get(sources, "semantic_ir", py.get(sources, "semantic", {}));
  var workflow_ir: any = py.get(sources, "workflow_ir", py.get(sources, "workflow", {}));
  var sync_ir: any = py.get(sources, "sync_ir", py.get(sources, "sync", {}));
  var execution_ir: any = py.get(sources, "execution_ir", py.get(sources, "execution", {}));
  var memory_ir: any = py.get(sources, "memory_ir", py.get(sources, "memory", {}));
  var runtime: any = reconstructRuntime(semantic_ir, workflow_ir, sync_ir, execution_ir, memory_ir, runtime_graph, runtime_type, tick);
  var browser: any = reconstructBrowserRuntime(py.get(sources, "browser_ir", py.get(sources, "browser", {})), py.get(sources, "interaction_ir", {}), py.get(sources, "identity", {}), py.get(sources, "session", {}), py.get(sources, "streaming", py.get(sources, "live", {})), py.get(sources, "dom", {}));
  var application: any = reconstructApplicationRuntime(py.get(sources, "application_ir", py.get(sources, "application", {})), workflow_ir, execution_ir, runtime_type);
  var session: any = reconstructRuntimeSession(py.get(sources, "session", {}), py.get(sources, "identity", {}), sync_ir, py.get(sources, "adaptive_memory", {}));
  var environment: any = buildRuntimeEnvironment(runtime_type, py.get(sources, "connectors", []), py.get(sources, "workers", []));
  var memory_rebuilt: any = reconstructRuntimeMemory(memory_ir, semantic_ir, py.get(sources, "lineage", py.get(memory_ir, "lineage", {})));
  var state: any = rebuildRuntimeState((((py.get(execution_ir, "queues") !== null && typeof py.get(execution_ir, "queues") === "object" && !Array.isArray(py.get(execution_ir, "queues")) && !(py.get(execution_ir, "queues") instanceof Set) && !(py.get(execution_ir, "queues") instanceof Map))) ? py.get(py.get(execution_ir, "queues", {}), "queue", []) : []), sync_ir, (((py.get(execution_ir, "mutations") !== null && typeof py.get(execution_ir, "mutations") === "object" && !Array.isArray(py.get(execution_ir, "mutations")) && !(py.get(execution_ir, "mutations") instanceof Set) && !(py.get(execution_ir, "mutations") instanceof Map))) ? py.get(py.get(execution_ir, "mutations", {}), "mutations", []) : []), py.get(execution_ir, "transactions", []), memory_rebuilt, (((py.get(sources, "lineage") !== null && typeof py.get(sources, "lineage") === "object" && !Array.isArray(py.get(sources, "lineage")) && !(py.get(sources, "lineage") instanceof Set) && !(py.get(sources, "lineage") instanceof Map))) ? py.get(py.get(sources, "lineage", {}), "lineage", []) : []), py.get(application, "workflows", []));
  var topology: any = reconstructRuntimeTopology(runtime_graph, py.get(sources, "workers", py.get(py.get(execution_ir, "federation", {}), "workers", [])), py.get(sources, "connectors", []), py.get(execution_ir, "federation", {}), sync_ir);
  var identity: any = reconstructRuntimeIdentity(py.get(sources, "identity", {}), py.get(sources, "session", {}), py.get(runtime, "runtime_id", ""), py.toStr((py.truthy(py.get(execution_ir, "transactions")) ? py.get(py.at(py.get(execution_ir, "transactions", [{}]), 0), "transaction_id", "") : "")), py.toStr(py.get(py.at(py.or2(py.get(sources, "workers"), () => ([{}])), 0), "worker_id", "")));
  var connectors: any = reconstructConnectorRuntime(py.get(sources, "connectors", []), py.get(sources, "live", py.get(sources, "live_ir", {})));
  var actions: any = py.get(execution_ir, "actions", []);
  // Direct kwargs->positional call (signature: events, actions, mutations,
  // synchronization, execution, recovery, replay, tick). The previous callKw
  // used a wrong parameter-order list, dropping every argument.
  var timeline: any = buildRuntimeTimeline(null, actions, py.get(state, "mutations", []), (((sync_ir !== null && typeof sync_ir === "object" && !Array.isArray(sync_ir) && !(sync_ir instanceof Set) && !(sync_ir instanceof Map))) ? py.enumerate(py.slice(py.get(sync_ir, "lineage", []), null, 100)).map(([i, _]: any) => ({"id": `sync:${py.toStr(i)}`, "tick": tick})) : []), actions, null, null, tick);
  var replay: any = buildRuntimeReplay(actions, py.get(execution_ir, "transactions", []), timeline, tick);
  var clone_result: Record<string, any> = {};
  if (py.truthy(clone)) {
    var source_body: any = {"runtime_graph": runtime_graph, "browser": browser, "application": application, "synchronization": sync_ir, "workflows": py.get(application, "workflows", []), "queues": py.get(state, "queues", [])};
    clone_result = cloneRuntimeEnvironment(source_body);
  }
  var fabrication: Record<string, any> = {};
  if (py.truthy(fabricate)) {
    fabrication = fabricateRuntimeReality(runtime, environment, browser, application);
  }
  var validation: any = validateReconstructedRuntime((!py.truthy(fabricate) ? runtime : py.get(fabrication, "runtime", runtime)), replay, topology, execution_ir, py.get(state, "mutations"));
  var prior_snapshot: any = py.get(stored, "snapshot", {});
  var recovery: any = recoverReconstructedRuntime(prior_snapshot);
  var snapshot: any = captureReconstructionSnapshot({"runtime": runtime, "browser": browser, "application": application, "topology": topology, "identities": identity, "workflows": py.get(application, "workflows", []), "replay_chains": py.get(replay, "replay_chains", []), "state": state});
  var payload: any = {"runtime": runtime, "browser": browser, "application": application, "session": session, "environment": environment, "memory": memory_rebuilt, "state": state, "topology": topology, "identity": identity, "connectors": connectors, "timeline": timeline, "replay": replay, "clone": clone_result, "fabrication": fabrication, "validation": validation, "recovery": recovery, "snapshot": snapshot, "bounded": true};
  py.setItem(payload, "reconstruction_ir", compileReconstructionRuntimeIr(payload));
  return payload;
}
export function runReconstructionForExtraction(reconstruction_runtime: any = true, memory_path: any = "", memory_key: any = "", sources: any = null, runtime_graph: any = null, runtime_type: any = "browser", tick: any = 0, fabricate_runtime: any = false, clone_runtime: any = false, merge_graph: any = true): any {
  if (!py.truthy(reconstruction_runtime)) {
    return {"enabled": false, "bounded": true};
  }
  var stored: Record<string, any> = {};
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    var loaded: any = loadReconstructionSnapshot(memory_path, memory_key);
    if (py.truthy(py.get(loaded, "available"))) {
      stored = py.get(loaded, "snapshot", stored);
    }
  }
  var result: any = runReconstructionRuntime(sources, stored, runtime_graph, runtime_type, tick, fabricate_runtime, clone_runtime);
  var store: any = captureReconstructionSnapshot({"runtime": py.get(result, "runtime", {}), "topology": py.get(result, "topology", {}), "identities": py.get(result, "identity", {}), "workflows": py.get(py.get(result, "application", {}), "workflows", []), "replay_chains": py.get(py.get(result, "replay", {}), "replay_chains", []), "state": py.get(result, "state", {})});
  var persisted: any = false;
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    saveReconstructionSnapshot(memory_path, store, memory_key);
    persisted = true;
  }
  var graph_ir: any = reconstructionRuntimeIrToGraph(py.get(result, "reconstruction_ir", {}));
  var unified_graph: Record<string, any> = {};
  if (py.truthy(merge_graph)) {
    unified_graph = buildRuntimeGraph([graph_ir]);
  }
  return {"enabled": true, "reconstruction": result, "reconstruction_ir": py.get(result, "reconstruction_ir", {}), "reconstruction_graph_ir": graph_ir, "unified_graph": unified_graph, "replay": py.get(result, "replay", {}), "validation": py.get(result, "validation", {}), "reconstruction_persisted": persisted, "bounded": true};
}
export { buildRuntimeEnvironment, buildRuntimeGraph, buildRuntimeReplay, buildRuntimeTimeline, captureReconstructionSnapshot, cloneRuntimeEnvironment, compileReconstructionRuntimeIr, fabricateRuntimeReality, loadReconstructionSnapshot, rebuildRuntimeState, reconstructApplicationRuntime, reconstructBrowserRuntime, reconstructConnectorRuntime, reconstructRuntime, reconstructRuntimeIdentity, reconstructRuntimeMemory, reconstructRuntimeSession, reconstructRuntimeTopology, reconstructionRuntimeIrToGraph, recoverReconstructedRuntime, saveReconstructionSnapshot, validateReconstructedRuntime };
