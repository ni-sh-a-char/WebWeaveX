import { replaySemanticJournal } from "./semanticJournal.js";
import { buildSemanticMemory } from "./semanticMemory.js";

export function replaySemanticState(
  state: Record<string, unknown>,
): Record<string, unknown> {
  const journal = replaySemanticJournal((state.journal as Record<string, unknown>[]) ?? []);
  const memory = buildSemanticMemory(
    (state.semantic as Record<string, unknown>) ?? {},
    (state.history as Record<string, unknown>[]) ?? [],
  );
  return { ...state, semantic: memory, journal, replayed: true, bounded: true };
}
