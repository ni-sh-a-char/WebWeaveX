import stringify from "fast-json-stable-stringify";
import type { RuntimeGraph } from "../contracts/graphContracts.js";
import { buildRuntimeMemory, stableMemoryHash } from "./runtimeMemory.js";
import { buildMemoryLineage } from "./memoryLineage.js";
import { buildRuntimeMemoryGraph } from "./runtimeMemoryGraph.js";

export function replayMemoryState(
  graph: RuntimeGraph,
  history: unknown[] = [],
): Record<string, unknown> {
  const mem = buildRuntimeMemory(graph, history);
  const lineage = buildMemoryLineage(
    history.map((h, i) => (typeof h === "object" && h ? { ...(h as object), tick: i } : { tick: i })),
  );
  const memory_graph = buildRuntimeMemoryGraph(graph, history);
  return {
    ...mem,
    lineage: lineage.lineage,
    memory_graph,
    replay_hash: stableMemoryHash(graph, history),
    bounded: true,
  };
}

export function validateMemoryReplay(
  original: Record<string, unknown>,
  replayed: Record<string, unknown>,
): boolean {
  return stringify(original.stable_hash) === stringify(replayed.stable_hash);
}
