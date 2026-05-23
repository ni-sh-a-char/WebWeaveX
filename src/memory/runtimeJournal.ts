import { appendSemanticJournalEvent } from "../semantic/semanticJournal.js";

export function appendRuntimeJournal(
  journal: Record<string, unknown>[],
  tick: number,
  payload: Record<string, unknown>,
): Record<string, unknown>[] {
  return appendSemanticJournalEvent(journal, { tick, ...payload, kind: "runtime" });
}
