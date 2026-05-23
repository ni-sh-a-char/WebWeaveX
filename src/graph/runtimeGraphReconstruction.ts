import { RuntimeGraphContract, type RuntimeGraph } from "../contracts/graphContracts.js";
import { reconstructGraphFromSources } from "../reconstruction/reconstructGraph.js";
import { graphFingerprint } from "./runtimeGraph.js";

export function reconstructGraphFromIr(sources: Record<string, unknown>): {
  graph: RuntimeGraph;
  fingerprint: string;
  bounded: boolean;
} {
  const graph = reconstructGraphFromSources(sources);
  return { graph, fingerprint: graphFingerprint(graph), bounded: true };
}

export function rebuildGraphFromPartial(partial: RuntimeGraph): RuntimeGraph {
  const normalized = RuntimeGraphContract.normalize(partial);
  const nodes = normalized.nodes.map((n, i) => ({
    ...n,
    id: n.id ?? `rebuilt:${i}`,
  }));
  return RuntimeGraphContract.normalize({ nodes, edges: normalized.edges, bounded: true });
}
