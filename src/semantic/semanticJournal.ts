import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";

const MAX_EVENTS = 10000;

export function appendSemanticJournalEvent(
  journal: Record<string, unknown>[],
  event: Record<string, unknown>,
): Record<string, unknown>[] {
  const entry = {
    ...event,
    event_id: computeDeterministicHash(event),
    bounded: true,
  };
  const next = [...journal, entry].slice(-MAX_EVENTS);
  return next.sort((a, b) => String(a.event_id).localeCompare(String(b.event_id)));
}

export function replaySemanticJournal(journal: Record<string, unknown>[]): Record<string, unknown> {
  return {
    events: journal,
    replay_hash: computeDeterministicHash({ events: journal }),
    bounded: journal.length <= MAX_EVENTS,
  };
}

export function createSemanticJournal(): {
  record: (event: Record<string, unknown>) => void;
  replay: () => { count: number; events: Record<string, unknown>[] };
} {
  const events: Record<string, unknown>[] = [];
  return {
    record(event) {
      events.push({ ...event, event_id: computeDeterministicHash(event) });
    },
    replay() {
      return { count: events.length, events: [...events] };
    },
  };
}
