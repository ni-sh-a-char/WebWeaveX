/**
 * Deterministic serializer — faithful port of core/serialize/deterministic_serializer.py.
 * Hand-written production module (protected).
 */
import * as py from "../runtime/pyCompat.js";

function normStr(value: string): string {
  return value.normalize("NFC");
}

function sortKeyJson(value: unknown): string {
  return py.jsonDumps(value, { ensureAscii: false, sortKeys: true, separators: [",", ":"] });
}

function stableValue(value: unknown, depth = 0): unknown {
  if (depth > 64) return py.toStr(value);
  if (typeof value === "string") return normStr(value);
  if (typeof value === "boolean" || value === null || value === undefined) return value ?? null;
  if (value instanceof py.PyFloat) {
    // Python float branch: integral floats convert exactly (before .15g),
    // fractional values round to 15 significant digits.
    if (!Number.isFinite(value.v)) return 0;
    if (Number.isInteger(value.v)) return value.v;
    return Number(value.v.toPrecision(15));
  }
  if (typeof value === "number") {
    if (Number.isInteger(value)) return value;
    if (!Number.isFinite(value)) return 0;
    // Python: float(format(value, ".15g"))
    return Number(value.toPrecision(15));
  }
  if (typeof value === "object" && !Array.isArray(value)) {
    const obj = value as Record<string, unknown>;
    const keys = Object.keys(obj).sort((a, b) =>
      py.codePointCompare(normStr(String(a)), normStr(String(b))),
    );
    const out: Record<string, unknown> = {};
    for (const k of keys) out[normStr(String(k))] = stableValue(obj[k], depth + 1);
    return out;
  }
  if (Array.isArray(value)) {
    const items = value.map((v) => stableValue(v, depth + 1));
    return items.slice().sort((a, b) => py.codePointCompare(sortKeyJson(a), sortKeyJson(b)));
  }
  return normStr(py.toStr(value));
}

export function dumpsDeterministic(value: unknown): string {
  return py.jsonDumps(stableValue(value), { ensureAscii: false, sortKeys: true, separators: [",", ":"] });
}

export const dumps_deterministic = dumpsDeterministic;
export const dumps_canonical = dumpsDeterministic;
export const dumps_canonical_v4 = dumpsDeterministic;
export const dumps_canonical_v5 = dumpsDeterministic;
export const dumpsCanonical = dumpsDeterministic;
export const dumpsCanonicalV4 = dumpsDeterministic;
export const dumpsCanonicalV5 = dumpsDeterministic;
