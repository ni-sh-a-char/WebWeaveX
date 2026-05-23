import stringify from "fast-json-stable-stringify";
import { computeKaalkaHashPayload } from "../crypto/kaalkaHash.js";
import { RuntimeGraphContract, type RuntimeGraph } from "../contracts/graphContracts.js";

export function buildRuntimeMemory(graph: RuntimeGraph, history: unknown[] = []): Record<string, unknown> {
  const normalized = RuntimeGraphContract.normalize(graph);
  const stable_hash = stableMemoryHash(normalized, history);
  return {
    memory: { graph: normalized, runtime_history: history },
    stable_hash,
    bounded: true,
  };
}

export function stableMemoryHash(graph: RuntimeGraph, history: unknown[] = []): string {
  return computeKaalkaHashPayload({
    graph: RuntimeGraphContract.normalize(graph),
    history_len: history.length,
  });
}

export function mergeRuntimeMemories(
  a: Record<string, unknown>,
  b: Record<string, unknown>,
): Record<string, unknown> {
  const ga = (a.memory as Record<string, unknown> | undefined)?.graph as RuntimeGraph | undefined;
  const gb = (b.memory as Record<string, unknown> | undefined)?.graph as RuntimeGraph | undefined;
  const merged: RuntimeGraph = {
    nodes: [...(ga?.nodes ?? []), ...(gb?.nodes ?? [])],
    edges: [...(ga?.edges ?? []), ...(gb?.edges ?? [])],
  };
  const ha = ((a.memory as Record<string, unknown> | undefined)?.runtime_history as unknown[]) ?? [];
  const hb = ((b.memory as Record<string, unknown> | undefined)?.runtime_history as unknown[]) ?? [];
  return buildRuntimeMemory(RuntimeGraphContract.normalize(merged), [...ha, ...hb]);
}

export function queryRuntimeMemory(mem: Record<string, unknown>, key: string): unknown {
  const m = mem.memory as Record<string, unknown> | undefined;
  return m?.[key];
}

export function replicateRuntimeMemory(mem: Record<string, unknown>): Record<string, unknown> {
  return JSON.parse(stringify(mem)) as Record<string, unknown>;
}
