/**
 * Deep structural equivalence — not string-only, not hash-only.
 */
import { createHash } from "node:crypto";

function stableKeySort(value: unknown): unknown {
  if (value === null || typeof value !== "object") return value;
  if (Array.isArray(value)) return value.map(stableKeySort);
  const obj = value as Record<string, unknown>;
  const sorted: Record<string, unknown> = {};
  for (const key of Object.keys(obj).sort()) {
    sorted[key] = stableKeySort(obj[key]);
  }
  return sorted;
}

function stableStringify(value: unknown): string {
  return JSON.stringify(stableKeySort(value));
}

function deepEqual(a: unknown, b: unknown): boolean {
  return stableStringify(a) === stableStringify(b);
}

export type DeepDiff = {
  path: string;
  expected: unknown;
  actual: unknown;
  kind: "missing" | "extra" | "type" | "value";
};

export type DeepCompareResult = {
  equal: boolean;
  diffs: DeepDiff[];
};

const MAX_DIFFS = 40;

export function deepCompare(expected: unknown, actual: unknown, basePath = ""): DeepCompareResult {
  if (deepEqual(expected, actual)) {
    return { equal: true, diffs: [] };
  }
  const diffs: DeepDiff[] = [];
  walk(expected, actual, basePath || "$", diffs);
  return { equal: diffs.length === 0, diffs };
}

function walk(expected: unknown, actual: unknown, path: string, diffs: DeepDiff[]): void {
  if (diffs.length >= MAX_DIFFS) return;
  if (deepEqual(expected, actual)) return;

  if (expected === null || expected === undefined) {
    if (actual !== expected) {
      diffs.push({ path, expected, actual, kind: "value" });
    }
    return;
  }
  if (actual === null || actual === undefined) {
    diffs.push({ path, expected, actual, kind: "missing" });
    return;
  }

  const expType = Array.isArray(expected) ? "array" : typeof expected;
  const actType = Array.isArray(actual) ? "array" : typeof actual;
  if (expType !== actType) {
    diffs.push({ path, expected, actual, kind: "type" });
    return;
  }

  if (Array.isArray(expected) && Array.isArray(actual)) {
    if (expected.length !== actual.length) {
      diffs.push({
        path: `${path}.length`,
        expected: expected.length,
        actual: actual.length,
        kind: "value",
      });
    }
    const len = Math.min(expected.length, actual.length);
    for (let i = 0; i < len; i++) {
      walk(expected[i], actual[i], `${path}[${i}]`, diffs);
      if (diffs.length >= MAX_DIFFS) return;
    }
    return;
  }

  if (typeof expected === "object" && typeof actual === "object") {
    const expObj = expected as Record<string, unknown>;
    const actObj = actual as Record<string, unknown>;
    const keys = new Set([...Object.keys(expObj), ...Object.keys(actObj)]);
    for (const key of [...keys].sort()) {
      if (!(key in expObj)) {
        diffs.push({ path: `${path}.${key}`, expected: undefined, actual: actObj[key], kind: "extra" });
        continue;
      }
      if (!(key in actObj)) {
        diffs.push({ path: `${path}.${key}`, expected: expObj[key], actual: undefined, kind: "missing" });
        continue;
      }
      walk(expObj[key], actObj[key], `${path}.${key}`, diffs);
      if (diffs.length >= MAX_DIFFS) return;
    }
    return;
  }

  diffs.push({ path, expected, actual, kind: "value" });
}

export function summarizeDiffs(diffs: DeepDiff[]): string[] {
  return diffs.map((d) => {
    const exp =
      d.expected === undefined
        ? "∅"
        : typeof d.expected === "object"
          ? JSON.stringify(d.expected).slice(0, 80)
          : String(d.expected).slice(0, 80);
    const act =
      d.actual === undefined
        ? "∅"
        : typeof d.actual === "object"
          ? JSON.stringify(d.actual).slice(0, 80)
          : String(d.actual).slice(0, 80);
    return `${d.path} (${d.kind}): py=${exp} js=${act}`;
  });
}
