import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";

export function createSemanticSnapshot(state: Record<string, unknown>): Record<string, unknown> {
  const snapshot_id = computeDeterministicHash(state);
  return {
    snapshot_id,
    state: { ...state },
    created_at: Date.now(),
    bounded: true,
  };
}

export function restoreSemanticSnapshot(snapshot: Record<string, unknown>): Record<string, unknown> {
  return { ...(snapshot.state as Record<string, unknown>), bounded: true };
}
