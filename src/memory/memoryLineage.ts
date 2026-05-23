import { computeKaalkaHashPayload } from "../crypto/kaalkaRuntime.js";

export type MemoryLineageEntry = {
  id: string;
  tick: number;
  parent_id: string | null;
  stable_hash: string;
};

export function buildMemoryLineage(
  history: Array<Record<string, unknown>>,
): { lineage: MemoryLineageEntry[]; bounded: boolean } {
  const lineage: MemoryLineageEntry[] = [];
  let parent: string | null = null;
  for (const [index, item] of history.entries()) {
    const tick = Number(item.tick ?? item.step ?? index);
    const id = computeKaalkaHashPayload({ tick, kind: item.kind ?? "step", parent });
    const stable_hash = computeKaalkaHashPayload(item);
    lineage.push({ id, tick, parent_id: parent, stable_hash });
    parent = id;
  }
  return { lineage, bounded: true };
}

export function verifyMemoryLineage(lineage: MemoryLineageEntry[]): boolean {
  for (let i = 1; i < lineage.length; i++) {
    if (lineage[i]!.parent_id !== lineage[i - 1]!.id) return false;
  }
  return true;
}
