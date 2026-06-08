import { buildRuntimeGraph } from "../graph/runtimeGraph.js";

export function buildSemanticWorldGraph(model: Record<string, unknown>): Record<string, unknown> {
  const entities = (model.entities as unknown[]) ?? [];
  const graph = buildRuntimeGraph({
    world: { entity_count: entities.length, model_id: model.world_model_id },
  });
  return { graph, entity_count: entities.length, bounded: true };
}
