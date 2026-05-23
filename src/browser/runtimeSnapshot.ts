import { computeKaalkaHashPayload } from "../crypto/kaalkaRuntime.js";
import { captureRuntime, type CapturedRuntime } from "./captureRuntime.js";
import type { RuntimeSessionEnvelope } from "./runtimeSession.js";

export type RuntimeSnapshot = CapturedRuntime & {
  snapshot_id: string;
  captured_at_tick: number;
  session_id?: string;
};

export async function captureRuntimeSnapshot(
  url: string,
  tick = 0,
  session?: RuntimeSessionEnvelope,
): Promise<RuntimeSnapshot> {
  const captured = await captureRuntime(url);
  const snapshot_id = computeKaalkaHashPayload({
    url: captured.url,
    dom_hash: captured.dom_hash,
    tick,
    session_id: session?.session_id ?? "",
  });
  return {
    ...captured,
    snapshot_id,
    captured_at_tick: tick,
    session_id: session?.session_id,
  };
}

export function compareRuntimeSnapshots(
  a: RuntimeSnapshot,
  b: RuntimeSnapshot,
): { equivalent: boolean; dom_match: boolean; route_match: boolean; bounded: boolean } {
  const dom_match = a.dom_hash === b.dom_hash;
  const route_match = JSON.stringify(a.routes) === JSON.stringify(b.routes);
  return { equivalent: dom_match && route_match, dom_match, route_match, bounded: true };
}
