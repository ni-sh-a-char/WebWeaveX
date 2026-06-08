import { mergeSemanticStates } from "./semanticMerge.js";

export function reconcileSemanticStates(
  states: Record<string, unknown>[],
): Record<string, unknown> {
  let acc: Record<string, unknown> = {};
  for (const s of states) {
    acc = (mergeSemanticStates(acc, s).state as Record<string, unknown>) ?? acc;
  }
  return { reconciled: acc, count: states.length, bounded: true };
}
