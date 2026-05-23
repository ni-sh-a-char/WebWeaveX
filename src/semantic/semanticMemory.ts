import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";

export class SemanticMemory {
  private store = new Map<string, unknown>();
  private lineage = new Map<string, Record<string, unknown>>();

  constructor(private maxEntries = 256) {}

  put(key: string, value: unknown, lineage?: Record<string, unknown>): void {
    if (this.store.size >= this.maxEntries) {
      const oldest = this.store.keys().next().value as string;
      this.store.delete(oldest);
      this.lineage.delete(oldest);
    }
    this.store.set(key, value);
    if (lineage) this.lineage.set(key, lineage);
  }

  get(key: string): unknown {
    return this.store.get(key);
  }

  snapshot(): Record<string, unknown> {
    return {
      keys: [...this.store.keys()].sort(),
      count: this.store.size,
      bounded: this.store.size <= this.maxEntries,
    };
  }
}

export function buildSemanticMemory(
  semantic: Record<string, unknown> = {},
  history: Record<string, unknown>[] = [],
): Record<string, unknown> {
  const inner = (semantic.semantic as Record<string, unknown>) ?? semantic;
  const concepts: string[] = [];
  const entities = (inner.entities as Record<string, unknown>)?.entities as Record<string, unknown>[] | undefined;
  for (const entity of entities ?? []) {
    const label = String(entity.label ?? entity.type ?? "");
    if (label) concepts.push(label);
  }
  return {
    semantic_id: computeDeterministicHash({ concepts: concepts.sort(), history_len: history.length }),
    concepts,
    history,
    bounded: true,
  };
}
