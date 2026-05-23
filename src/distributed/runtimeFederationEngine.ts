import { buildRuntimeGraph } from "../graph/runtimeGraph.js";

const MAX_RUNTIMES = 1000;

export function federateExtractionRuntimes(
  runtimes: Record<string, unknown>[] = [],
): Record<string, unknown> {
  const graphs = runtimes
    .slice(0, MAX_RUNTIMES)
    .filter((r) => (r.nodes as unknown[])?.length || (r.edges as unknown[])?.length);
  const sources: Record<string, unknown> = {};
  graphs.forEach((g, i) => {
    sources[`runtime_${i}`] = g;
  });
  const topology =
    graphs.length > 0
      ? buildRuntimeGraph(sources)
      : { nodes: [], edges: [], bounded: true };
  return { topology, runtime_count: runtimes.length, bounded: true };
}
