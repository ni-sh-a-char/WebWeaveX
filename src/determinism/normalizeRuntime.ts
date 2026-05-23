import { RuntimeGraphContract, type RuntimeGraph } from "../contracts/graphContracts.js";

const STRIP_KEYS = new Set(["timestamp", "created_at", "updated_at", "nonce", "request_id"]);

export function normalizeRuntimeState(state: Record<string, unknown>): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  const keys = Object.keys(state).sort();
  for (const k of keys) {
    if (STRIP_KEYS.has(k)) continue;
    const v = state[k];
    if (v && typeof v === "object" && !Array.isArray(v)) {
      out[k] = normalizeRuntimeState(v as Record<string, unknown>);
    } else if (Array.isArray(v)) {
      out[k] = v.map((item) =>
        item && typeof item === "object"
          ? normalizeRuntimeState(item as Record<string, unknown>)
          : item,
      );
    } else {
      out[k] = v;
    }
  }
  return out;
}

export function normalizeRuntimeGraph(graph: RuntimeGraph): RuntimeGraph {
  return RuntimeGraphContract.normalize(graph);
}
