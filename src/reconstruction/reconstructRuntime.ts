import { computeKaalkaHashPayload } from "../crypto/kaalkaHash.js";
import { RuntimeGraphContract, type RuntimeGraph } from "../contracts/graphContracts.js";
import type { ExtractionEnvelope } from "../contracts/runtimeContracts.js";

export function reconstructRuntime(
  sources: Record<string, unknown>,
  runtimeType = "browser",
  tick = 0,
): Record<string, unknown> {
  const graph = (sources.extraction as ExtractionEnvelope | undefined)?.unified_runtime_graph ?? {
    nodes: [],
    edges: [],
  };
  const normalized = RuntimeGraphContract.normalize(graph as RuntimeGraph);
  const runtime_id = computeKaalkaHashPayload({ runtimeType, tick, nodes: normalized.nodes.length });
  return {
    runtime: { runtime_id, runtime_type: runtimeType, tick },
    graph: normalized,
    bounded: true,
  };
}

export function replayRuntime(extraction: ExtractionEnvelope): ExtractionEnvelope {
  return JSON.parse(JSON.stringify(extraction)) as ExtractionEnvelope;
}

export function rebuildExecutionGraph(extraction: ExtractionEnvelope): RuntimeGraph {
  return RuntimeGraphContract.normalize(extraction.unified_runtime_graph ?? { nodes: [], edges: [] });
}
