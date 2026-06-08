import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";

export function buildSemanticLineage(
  events: Array<Record<string, unknown>>,
): Record<string, unknown> {
  const lineage = events.map((e, i) => ({
    index: i,
    kind: e.kind ?? "event",
    tick: e.tick ?? i,
    hash: computeDeterministicHash(e),
  }));
  return {
    lineage,
    lineage_id: computeDeterministicHash({ lineage }),
    bounded: true,
  };
}
