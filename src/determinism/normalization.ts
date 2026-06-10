import { RuntimeGraphContract, type RuntimeGraph } from "../contracts/graphContracts.js";
import { PyFloat, codePointCompare, pyFloatRepr } from "../runtime/pyCompat.js";

/**
 * Cross-language numeric canonicalization: PyFloat unwraps to a plain number,
 * non-finite numbers become null (JSON.stringify semantics, shared by Python
 * and Dart). Integral floats are already plain integers in JS.
 */
function canonicalizeNumber(v: unknown): unknown {
  const n = v instanceof PyFloat ? v.v : v;
  if (typeof n === "number" && !Number.isFinite(n)) return null;
  return n;
}

/**
 * Canonical stable stringify: code-point key order (Python `sorted`),
 * Python float repr for non-integral numbers. Replaces
 * fast-json-stable-stringify, whose UTF-16 key sort and `''+number`
 * formatting diverge from Python.
 */
function stableStringify(value: unknown): string {
  const v = canonicalizeNumber(value);
  if (v === null || v === undefined) return "null";
  if (typeof v === "boolean") return v ? "true" : "false";
  if (typeof v === "number") {
    // Integral values < 2^63 print as integers (the exact int-conversion zone
    // in Python/Dart); everything else uses Python float repr.
    return Number.isInteger(v) && Math.abs(v) < 9223372036854775808
      ? String(v)
      : pyFloatRepr(v);
  }
  if (typeof v === "string") return JSON.stringify(v);
  if (typeof v === "object" && typeof (v as { toJSON?: unknown }).toJSON === "function") {
    return stableStringify((v as { toJSON: () => unknown }).toJSON());
  }
  if (Array.isArray(v)) {
    return `[${v.map((item) => stableStringify(item)).join(",")}]`;
  }
  if (typeof v === "object") {
    const obj = v as Record<string, unknown>;
    const keys = Object.keys(obj).sort(codePointCompare);
    const parts: string[] = [];
    for (const k of keys) {
      if (obj[k] === undefined) continue;
      parts.push(`${JSON.stringify(k)}:${stableStringify(obj[k])}`);
    }
    return `{${parts.join(",")}}`;
  }
  return JSON.stringify(v);
}

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
  for (const k of Object.keys(obj).sort(codePointCompare)) {
    if (VOLATILE_RUNTIME_KEYS.has(k)) continue;
    const v = obj[k];
    if (v instanceof PyFloat) {
      sorted[k] = canonicalizeNumber(v);
    } else if (v && typeof v === "object" && !Array.isArray(v)) {
      sorted[k] = stableSortKeys(v as Record<string, unknown>);
    } else if (Array.isArray(v)) {
      sorted[k] = v.map((item) =>
        item && typeof item === "object" && !Array.isArray(item) && !(item instanceof PyFloat)
          ? stableSortKeys(item as Record<string, unknown>)
          : canonicalizeNumber(item),
      );
    } else {
      sorted[k] = canonicalizeNumber(v);
    }
  }
  return sorted;
}

/** Canonical JSON string for cross-language parity. */
export function stableSerialize(value: unknown): string {
  if (typeof value === "string") {
    return normalizeRuntimeValue(value);
  }
  const unwrapped = canonicalizeNumber(value);
  if (unwrapped && typeof unwrapped === "object") {
    if (Array.isArray(unwrapped)) {
      // Arrays serialize as keyed objects (historical fast-json-stable-stringify
      // shape, mirrored by Python and Dart stable_serialize).
      const keyed: Record<string, unknown> = {};
      unwrapped.forEach((item, i) => {
        keyed[String(i)] =
          item && typeof item === "object" && !Array.isArray(item) && !(item instanceof PyFloat)
            ? stableSortKeys(item as Record<string, unknown>)
            : canonicalizeNumber(item);
      });
      return stableStringify(keyed);
    }
    return stableStringify(stableSortKeys(unwrapped as Record<string, unknown>));
  }
  return stableStringify(unwrapped);
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
