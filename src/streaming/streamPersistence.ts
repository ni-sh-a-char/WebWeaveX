import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { encryptValue, decryptValue } from "../crypto/kaalkaRuntime.js";
import type { StreamEvent } from "./streamCapture.js";
import { normalizeStreamEvents } from "./streamCapture.js";

export function saveStreamRuntime(
  path: string,
  payload: { events: StreamEvent[] },
  key: string,
): void {
  const enc = encryptValue(payload, key);
  writeFileSync(path, JSON.stringify(enc), "utf-8");
}

export function loadStreamRuntime(path: string, key: string): { events: StreamEvent[] } {
  if (!existsSync(path)) return { events: [] };
  try {
    const raw = JSON.parse(readFileSync(path, "utf-8")) as { encrypted: string };
    const dec = JSON.parse(decryptValue(raw.encrypted, key).decrypted) as { events: StreamEvent[] };
    return { events: normalizeStreamEvents(dec.events ?? []) };
  } catch {
    return { events: [] };
  }
}

export function mergeStreamRuntimes(
  left: { events: StreamEvent[] },
  right: { events: StreamEvent[] },
): { events: StreamEvent[] } {
  return { events: normalizeStreamEvents([...left.events, ...right.events]) };
}

export function mergeStreamRuntimePayloads(
  payloads: Array<Record<string, unknown>>,
): { events: StreamEvent[]; stream_count: number; bounded: boolean } {
  const events = payloads.flatMap((p) => (p.events as StreamEvent[]) ?? []);
  const normalized = normalizeStreamEvents(events).sort(
    (a, b) => Number(a.timestamp ?? 0) - Number(b.timestamp ?? 0),
  );
  return { events: normalized, stream_count: payloads.length, bounded: true };
}
