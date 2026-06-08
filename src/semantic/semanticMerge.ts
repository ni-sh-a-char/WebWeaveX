import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";

export function mergeSemanticStates(
  left: Record<string, unknown>,
  right: Record<string, unknown>,
): Record<string, unknown> {
  const keys = [...new Set([...Object.keys(left), ...Object.keys(right)])].sort();
  const state: Record<string, unknown> = {};
  let conflict = false;
  for (const k of keys) {
    if (k in left && k in right && left[k] !== right[k]) {
      state[k] = { conflict: true, left: left[k], right: right[k] };
      conflict = true;
    } else {
      state[k] = right[k] ?? left[k];
    }
  }
  return {
    state,
    merge_id: computeDeterministicHash({ keys, left, right }),
    deterministic: !conflict,
    bounded: true,
  };
}
