import { computeKaalkaHashPayload } from "../crypto/kaalkaRuntime.js";
import { RuntimeGraphContract, type RuntimeGraph } from "../contracts/graphContracts.js";
import type { ExtractionEnvelope } from "../contracts/runtimeContracts.js";
import { reconstructRuntimeGraph } from "./reconstructGraph.js";
import { reconstructMemoryFromEnvelope } from "./reconstructMemory.js";
import { reconstructBrowserState } from "./reconstructBrowser.js";
import { reconstructReplayState } from "./reconstructReplay.js";

export function reconstructRuntime(
  sources: Record<string, unknown>,
  runtimeType = "browser",
  tick = 0,
): Record<string, unknown> {
  const extraction = sources.extraction as ExtractionEnvelope | undefined;
  const graph = extraction
    ? reconstructRuntimeGraph(extraction)
    : RuntimeGraphContract.normalize({ nodes: [], edges: [] });
  const normalized = RuntimeGraphContract.normalize(graph);
  const runtime_id = computeKaalkaHashPayload({ runtimeType, tick, nodes: normalized.nodes.length });
  const memory = extraction
    ? reconstructMemoryFromEnvelope(extraction as Record<string, unknown>)
    : { bounded: true };
  const browser = extraction ? reconstructBrowserState(extraction) : { bounded: true };
  return {
    runtime: { runtime_id, runtime_type: runtimeType, tick },
    graph: normalized,
    memory,
    browser,
    reconstructed: true,
    bounded: true,
  };
}

export function replayRuntime(extraction: ExtractionEnvelope): ExtractionEnvelope {
  return reconstructReplayState(extraction).replayed;
}

export function rebuildExecutionGraph(extraction: ExtractionEnvelope): RuntimeGraph {
  return reconstructRuntimeGraph(extraction);
}

export { reconstructReplayState } from "./reconstructReplay.js";
export { reconstructRuntimeGraph, reconstructGraphFromSources } from "./reconstructGraph.js";
export { reconstructMemoryFromEnvelope, reconstructMemoryGraph } from "./reconstructMemory.js";
export { reconstructBrowserState } from "./reconstructBrowser.js";
