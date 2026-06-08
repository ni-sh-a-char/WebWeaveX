import { compileWorldModel } from "./worldModelCompile.js";
import { buildSemanticWorldGraph } from "./semanticWorldGraph.js";

export function runWorldModelRuntime(snapshot: Record<string, unknown>): Record<string, unknown> {
  const compiled = compileWorldModel(snapshot);
  const graph = buildSemanticWorldGraph(compiled);
  return { ...compiled, graph, runtime: "world_model", bounded: true };
}
