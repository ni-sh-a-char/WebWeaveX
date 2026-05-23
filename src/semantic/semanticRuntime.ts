import { buildSemanticMemory } from "./semanticMemory.js";
import { appendSemanticJournalEvent } from "./semanticJournal.js";

export function runSemanticRuntime(
  state: Record<string, unknown> = {},
  event: Record<string, unknown> = {},
): Record<string, unknown> {
  const journal = (state.journal as Record<string, unknown>[]) ?? [];
  const nextJournal = appendSemanticJournalEvent(journal, event);
  const memory = buildSemanticMemory(
    (state.semantic as Record<string, unknown>) ?? {},
    (state.history as Record<string, unknown>[]) ?? [],
  );
  return { semantic: memory, journal: nextJournal, bounded: true };
}
