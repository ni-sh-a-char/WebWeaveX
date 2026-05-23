import stringify from "fast-json-stable-stringify";
import { RuntimeGraphContract, type RuntimeGraph } from "../contracts/graphContracts.js";

/** Volatile keys stripped before stable serialization (all nesting levels). */
export const VOLATILE_RUNTIME_KEYS = new Set([
  "timestamp",
  "created_at",
  "updated_at",
  "nonce",
  "request_id",
  "csrf",
  "generated_at",
  "runtime_id",
  "random",
  "uuid",
]);

/** NFKC + CRLF normalization — applied before Kaalka hash/encrypt. */
export function normalizeRuntimeValue(value: string): string {
  return value
    .normalize("NFKC")
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n")
    .replace(/\s+$/, "");
}

export function stableSortKeys(obj: Record<string, unknown>): Record<string, unknown> {
  const sorted: Record<string, unknown> = {};
  for (const k of Object.keys(obj).sort()) {
    if (VOLATILE_RUNTIME_KEYS.has(k)) continue;
    const v = obj[k];
    if (v && typeof v === "object" && !Array.isArray(v)) {
      sorted[k] = stableSortKeys(v as Record<string, unknown>);
    } else if (Array.isArray(v)) {
      sorted[k] = v.map((item) =>
        item && typeof item === "object" && !Array.isArray(item)
          ? stableSortKeys(item as Record<string, unknown>)
          : item,
      );
    } else if (typeof v === "number" && Number.isFinite(v)) {
      sorted[k] = v;
    } else {
      sorted[k] = v;
    }
  }
  return sorted;
}

/** Canonical JSON string for cross-language parity. */
export function stableSerialize(value: unknown): string {
  if (typeof value === "string") {
    return normalizeRuntimeValue(value);
  }
  if (value && typeof value === "object") {
    return stringify(stableSortKeys(value as Record<string, unknown>));
  }
  return stringify(value);
}

export function normalizeRuntimeState(state: Record<string, unknown>): Record<string, unknown> {
  return stableSortKeys(state);
}

export function normalizeRuntimeGraph(graph: RuntimeGraph): RuntimeGraph {
  return RuntimeGraphContract.normalize(graph);
}

export function normalizeNetwork(
  events: Array<{ url: string; method: string }>,
): Array<{ url: string; method: string }> {
  return [...events].sort((a, b) =>
    `${a.method}|${a.url}`.localeCompare(`${b.method}|${b.url}`),
  );
}
