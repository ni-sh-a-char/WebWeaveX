import type { RuntimeGraph } from "../contracts/graphContracts.js";
import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";

export function buildSemanticGraphLineage(graphs: RuntimeGraph[]): Record<string, unknown> {
  return {
    graph_count: graphs.length,
    lineage_id: computeDeterministicHash({
      fingerprints: graphs.map((g) => g.nodes.length + g.edges.length),
    }),
    bounded: true,
  };
}

export function querySemanticGraphCognition(
  graph: RuntimeGraph,
  predicate: (node: RuntimeGraph["nodes"][number]) => boolean,
): Record<string, unknown> {
  const matches = graph.nodes.filter(predicate);
  return { matches: matches.length, nodes: matches, bounded: true };
}
