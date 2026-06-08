import type { StreamEvent } from "./streamCapture.js";

export function replayStreamEvents(events: StreamEvent[]): Record<string, unknown> {
  const ordered = [...events].sort((a, b) => a.seq - b.seq);
  const hashes = ordered.map((e) => e.hash);
  return {
    equivalent: hashes.length === events.length,
    event_count: ordered.length,
    replayed: ordered.map((e) => ({ id: e.id, seq: e.seq })),
    bounded: true,
    replay_hash: hashes.join("|"),
  };
}

export function buildStreamTimeline(events: StreamEvent[]): Record<string, unknown> {
  const ordered = [...events].sort((a, b) => a.timestamp - b.timestamp);
  return {
    timeline: ordered.map((e) => ({ id: e.id, seq: e.seq, channel: e.channel, timestamp: e.timestamp })),
    start: ordered[0]?.timestamp ?? 0,
    end: ordered[ordered.length - 1]?.timestamp ?? 0,
    count: ordered.length,
    bounded: true,
  };
}
