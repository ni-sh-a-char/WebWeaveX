import { RuntimeGraphContract, type RuntimeGraph } from "../contracts/graphContracts.js";
import { graphFingerprint } from "../graph/runtimeGraph.js";
import type { ExtractionEnvelope } from "../contracts/runtimeContracts.js";

export function reconstructRuntimeGraph(
  extraction: ExtractionEnvelope | Record<string, unknown>,
): RuntimeGraph {
  const env = extraction as ExtractionEnvelope;
  const graph = env.unified_runtime_graph ?? env.graph ?? { nodes: [], edges: [] };
  return RuntimeGraphContract.normalize(graph as RuntimeGraph);
}

export function reconstructGraphFromSources(sources: Record<string, unknown>): RuntimeGraph {
  const nodes: RuntimeGraph["nodes"] = [];
  const edges: RuntimeGraph["edges"] = [];
  let idx = 0;
  for (const [kind, payload] of Object.entries(sources).sort(([a], [b]) => a.localeCompare(b))) {
    nodes.push({ id: `recon:${kind}:${idx}`, type: kind, payload });
    idx += 1;
  }
  return RuntimeGraphContract.normalize({ nodes, edges, bounded: true });
}

export function graphReconstructionFingerprint(graph: RuntimeGraph): string {
  return graphFingerprint(graph);
}
