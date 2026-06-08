/**
 * Converted from Python: core/connectors/live_runtime_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractApiRuntime } from "./apiConnectorEngine.js";
import { extractCicdRuntime } from "./cicdConnectorEngine.js";
import { extractContainerRuntime } from "./containerConnectorEngine.js";
import { extractDatabaseRuntime } from "./databaseConnectorEngine.js";
import { extractFilesystemRuntime } from "./filesystemConnectorEngine.js";
import { extractIdeRuntime } from "./ideConnectorEngine.js";
import { extractKubernetesRuntime } from "./kubernetesConnectorEngine.js";
import { loadLiveRuntime } from "./liveRuntimeMemoryEngine.js";
import { rememberLiveRuntime } from "./liveRuntimeMemoryEngine.js";
import { saveLiveRuntime } from "./liveRuntimeMemoryEngine.js";
import { extractRuntimeStreams } from "./runtimeStreamConnectorEngine.js";
import { extractTelemetryRuntime } from "./telemetryConnectorEngine.js";
import { buildLiveTopologyGraph, compileLiveRuntimeIr, liveRuntimeIrToGraph } from "../ir/liveRuntimeIr.js";
import { buildRuntimeGraph } from "../runtime_graph/runtimeGraphEngine.js";

export function runLiveRuntime(config: any = null, snapshot: any = null, memory: any = null, tick: any = 0): any {
  config = py.or2(config, () => ({}));
  var snap: any = py.or2(snapshot, () => ({}));
  memory = py.pyDict(py.or2(memory, () => ({})));
  var database: any = extractDatabaseRuntime(py.get(config, "database_type", "postgresql"), py.get(snap, "database"));
  var api: any = extractApiRuntime(py.get(config, "api_type", "rest"), py.get(snap, "api"));
  var streams: any = extractRuntimeStreams(py.get(config, "stream_types"), snap);
  var filesystem: any = extractFilesystemRuntime(py.get(config, "filesystem_root", "."), py.get(snap, "filesystem"));
  var containers: any = extractContainerRuntime(py.get(config, "container_runtime", "docker"), py.get(snap, "containers"));
  var kubernetes: any = extractKubernetesRuntime(py.get(snap, "kubernetes"));
  var cicd: any = extractCicdRuntime(py.get(config, "cicd_provider", "github_actions"), py.get(snap, "cicd"));
  var telemetry: any = extractTelemetryRuntime(py.get(config, "telemetry_backends"), py.get(snap, "telemetry"));
  var ide: any = extractIdeRuntime(py.get(config, "ide", "vscode"), py.get(snap, "ide"));
  var payload: any = {"database": database, "api": api, "streams": streams, "filesystem": filesystem, "containers": containers, "kubernetes": kubernetes, "cicd": cicd, "telemetry": telemetry, "ide": ide, "tick": tick, "bounded": true};
  var graph: any = buildLiveTopologyGraph(payload);
  py.setItem(payload, "graph", graph);
  py.setItem(payload, "sync_state", {"stream_lineage": streams, "topology": graph});
  var stream_lineage: any[] = [];
  var stream: any;
  for (stream of py.iter(py.get(streams, "streams", []))) {
    py.extend(stream_lineage, py.get(stream, "event_lineage", []));
  }
  var updated_memory: any = rememberLiveRuntime(memory, {"connector_states": {"database": database, "api": api, "containers": containers, "kubernetes": kubernetes}, "stream_states": streams, "topology": graph, "telemetry_lineage": py.get(telemetry, "distributed_correlations", []), "snapshots": payload, "stream_lineage": stream_lineage});
  py.setItem(payload, "memory", updated_memory);
  py.setItem(payload, "replay", {"stream_lineage": stream_lineage, "topology": graph, "replayed": true, "bounded": true});
  py.setItem(payload, "live_ir", compileLiveRuntimeIr(payload));
  return payload;
}
export function runLiveForExtraction(live_runtime: any = true, memory_path: any = "", memory_key: any = "", config: any = null, snapshot: any = null, tick: any = 0, merge_graph: any = true): any {
  if (!py.truthy(live_runtime)) {
    return {"enabled": false, "bounded": true};
  }
  var memory: Record<string, any> = {};
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    var loaded: any = loadLiveRuntime(memory_path, memory_key);
    if (py.truthy(py.get(loaded, "available"))) {
      memory = py.get(loaded, "memory", memory);
    }
  }
  var result: any = runLiveRuntime(config, snapshot, memory, tick);
  var persisted: any = false;
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    saveLiveRuntime(memory_path, py.get(result, "memory", {}), memory_key);
    persisted = true;
  }
  var graph_ir: any = liveRuntimeIrToGraph(py.get(result, "live_ir", {}));
  var unified_graph: Record<string, any> = {};
  if (py.truthy(merge_graph)) {
    unified_graph = buildRuntimeGraph([graph_ir]);
  }
  return {"enabled": true, "live": result, "live_ir": py.get(result, "live_ir", {}), "live_graph_ir": graph_ir, "unified_graph": unified_graph, "replay": py.get(result, "replay", {}), "memory_persisted": persisted, "bounded": true};
}
export { buildLiveTopologyGraph, buildRuntimeGraph, compileLiveRuntimeIr, extractApiRuntime, extractCicdRuntime, extractContainerRuntime, extractDatabaseRuntime, extractFilesystemRuntime, extractIdeRuntime, extractKubernetesRuntime, extractRuntimeStreams, extractTelemetryRuntime, liveRuntimeIrToGraph, loadLiveRuntime, rememberLiveRuntime, saveLiveRuntime };
