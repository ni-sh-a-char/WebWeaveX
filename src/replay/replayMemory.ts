import { buildRuntimeMemory, stableMemoryHash } from "../memory/runtimeMemory.js";
import type { RuntimeGraph } from "../contracts/graphContracts.js";

export function replayRuntimeMemory(
  graph: RuntimeGraph,
  history: unknown[] = [],
): Record<string, unknown> {
  return buildRuntimeMemory(graph, history);
}

export function validateMemoryReplayEquivalence(
  original: Record<string, unknown>,
  replayed: Record<string, unknown>,
): { equivalent: boolean; stable_hash_match: boolean; bounded: boolean } {
  const o = original.stable_hash as string | undefined;
  const r = replayed.stable_hash as string | undefined;
  return {
    equivalent: o != null && o === r,
    stable_hash_match: o === r,
    bounded: true,
  };
}

export function memoryReplayHash(graph: RuntimeGraph, history: unknown[] = []): string {
  return stableMemoryHash(graph, history);
}
