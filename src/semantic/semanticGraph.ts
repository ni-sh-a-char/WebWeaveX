import { buildRuntimeGraph } from "../graph/runtimeGraph.js";

export function buildSemanticGraph(entities: Record<string, unknown>[]): Record<string, unknown> {
  const sources: Record<string, unknown> = {};
  entities.forEach((e, i) => {
    sources[`entity_${i}`] = e;
  });
  return buildRuntimeGraph(sources);
}
