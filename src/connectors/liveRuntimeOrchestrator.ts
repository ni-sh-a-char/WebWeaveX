import { extractApiRuntime } from "./apiConnector.js";
import { extractCicdRuntime } from "./cicdConnector.js";
import { extractContainerRuntime } from "./containerConnector.js";
import { extractDatabaseRuntime } from "./databaseConnector.js";
import { extractFilesystemRuntime } from "./filesystemConnector.js";
import { extractIdeRuntime } from "./ideConnector.js";
import { extractKubernetesRuntime } from "./kubernetesConnector.js";
import { extractRuntimeStreamRuntime } from "./runtimeStreamConnector.js";
import { extractTelemetryRuntime } from "./telemetryConnector.js";
import { loadLiveRuntimeMemory, rememberLiveRuntime, saveLiveRuntimeMemory } from "./liveRuntimeMemory.js";
import { buildRuntimeGraph } from "../graph/runtimeGraph.js";

export function runLiveRuntime(config: Record<string, unknown> = {}): Record<string, unknown> {
  const key = String(config.key ?? "default");
  const parts: Record<string, unknown> = {
    api: extractApiRuntime(String(config.api_type ?? "rest"), (config.api as Record<string, unknown>) ?? {}),
    database: extractDatabaseRuntime(
      String(config.database_type ?? "postgresql"),
      (config.database as Record<string, unknown>) ?? {},
    ),
    filesystem: extractFilesystemRuntime(String(config.root ?? ".")),
    kubernetes: extractKubernetesRuntime((config.kubernetes as Record<string, unknown>) ?? {}),
    container: extractContainerRuntime(String(config.container_runtime ?? "docker")),
    cicd: extractCicdRuntime(String(config.cicd_provider ?? "github_actions")),
    ide: extractIdeRuntime(String(config.ide ?? "vscode")),
    telemetry: extractTelemetryRuntime(),
    streams: extractRuntimeStreamRuntime(),
  };
  const graph = buildRuntimeGraph(parts);
  rememberLiveRuntime(key, { graph, parts });
  if (config.save_path && config.encryption_key) {
    saveLiveRuntimeMemory(key, { graph, parts }, String(config.encryption_key), String(config.save_path));
  }
  return { graph, parts, bounded: true };
}

export function runLiveForExtraction(
  extraction: Record<string, unknown>,
  config: Record<string, unknown> = {},
): Record<string, unknown> {
  const live = runLiveRuntime(config);
  return { ...extraction, live_runtime: live, bounded: true };
}

export { loadLiveRuntimeMemory, rememberLiveRuntime, saveLiveRuntimeMemory };
