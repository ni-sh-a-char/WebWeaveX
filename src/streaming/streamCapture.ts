import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";

export type StreamEvent = {
  id: string;
  seq: number;
  timestamp: number;
  channel: string;
  source: string;
  direction: "in" | "out";
  payload: string;
  correlation_id: string;
  hash: string;
};

export function makeStreamEvent(
  seq: number,
  channel: string,
  direction: "in" | "out",
  payload: string,
  correlationId: string,
  timestamp = seq,
  source = channel,
): StreamEvent {
  const hash = computeDeterministicHash({ seq, channel, direction, payload, correlationId, timestamp, source });
  return {
    id: `stream_${seq}`,
    seq,
    timestamp,
    channel,
    source,
    direction,
    payload,
    correlation_id: correlationId,
    hash,
  };
}

type LooseEvent = Partial<StreamEvent> & {
  timestamp?: number;
  source?: string;
  connection_id?: string;
};

export function normalizeStreamEvents(events: LooseEvent[]): StreamEvent[] {
  return events
    .map((e, i) => {
      if (e.id && e.hash && e.timestamp != null) return e as StreamEvent;
      const ts = e.timestamp ?? i;
      const src = e.source ?? e.channel ?? "default";
      const dir = (e.direction ?? "in") as "in" | "out";
      return makeStreamEvent(
        e.seq ?? i,
        e.channel ?? src,
        dir,
        e.payload ?? "{}",
        e.correlation_id ?? e.connection_id ?? "c",
        ts,
        src,
      );
    })
    .sort((a, b) => a.timestamp - b.timestamp);
}
