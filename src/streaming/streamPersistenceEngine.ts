/**
 * Converted from Python: core/streaming/stream_persistence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeKaalkaHashPayload } from "../crypto/kaalkaHashEngine.js";
import { decryptSessionState, encryptSessionState } from "../crypto/kaalkaSessionEngine.js";
import { normalizeStreamEvents } from "./streamCaptureEngine.js";

export let MAX_STREAMS: any = 1000;
export function saveStreamRuntime(path: any, runtime: any, key: any): any {
  var payload: any = {"runtime": runtime, "events": normalizeStreamEvents([...py.iter(py.get(runtime, "events", []))]), "bounded": true};
  var encrypted: any = encryptSessionState(payload, key);
  var target: any = py.path(path);
  target.parent.mkdir(true, true);
  target.write_text(py.jsonDumps(encrypted, {sortKeys: true}), "utf-8");
  return {"saved": true, "path": py.toStr(target), "algorithm": "kaalka", "bounded": true};
}
export function loadStreamRuntime(path: any, key: any): any {
  var target: any = py.path(path);
  if (!py.truthy(target.exists())) {
    return {"available": false, "runtime": {"events": [], "bounded": true}, "bounded": true};
  }
  var encrypted: any = py.jsonLoads(target.read_text("utf-8"));
  var decrypted: any = decryptSessionState(encrypted, key);
  var session_payload: any = py.get(decrypted, "session", {});
  return {"available": true, "runtime": py.get(session_payload, "runtime", {}), "events": py.get(session_payload, "events", []), "algorithm": "kaalka", "bounded": true};
}
export function createStreamCheckpoint(runtime: any, position: any): any {
  var events: any = [...py.iter(py.get(runtime, "events", []))];
  var bounded_position: any = py.min([py.max([py.toInt(position), 0]), py.len(events)]);
  var checkpoint: any = {"position": bounded_position, "events": py.slice(events, null, bounded_position), "runtime_state": py.pyDict(py.get(runtime, "runtime_state", {})), "checkpoint_hash": computeKaalkaHashPayload({"position": bounded_position, "events": py.slice(events, null, bounded_position), "runtime_state": py.get(runtime, "runtime_state", {})}), "bounded": true};
  return checkpoint;
}
export function restoreStreamCheckpoint(checkpoint: any): any {
  var events: any = [...py.iter(py.get(checkpoint, "events", []))];
  return {"position": py.toInt(py.get(checkpoint, "position", 0)), "events": events, "runtime_state": py.pyDict(py.get(checkpoint, "runtime_state", {})), "checkpoint_hash": py.get(checkpoint, "checkpoint_hash", ""), "bounded": true};
}
export function mergeStreamRuntimes(streams: any): any {
  var merged_events: any[] = [];
  var stream_index: any;
  var stream: any;
  for ([stream_index, stream] of py.enumerate(py.slice(streams, null, MAX_STREAMS))) {
    var source: any = py.toStr(py.get(stream, "source", `stream_${py.toStr(stream_index)}`));
    var events: any = normalizeStreamEvents([...py.iter(py.get(stream, "events", []))]);
    var event: any;
    for (event of py.iter(events)) {
      var enriched: any = py.pyDict(event);
      py.setItem(enriched, "stream_source", source);
      py.listAppend(merged_events, enriched);
    }
  }
  merged_events = py.sorted(merged_events, {key: ((item: any) => [py.toInt(py.get(item, "timestamp", 0)), py.toStr(py.get(item, "stream_source", "")), py.toStr(py.get(item, "id", ""))]) as (item: any) => any});
  return {"events": merged_events, "stream_count": py.min([py.len(streams), MAX_STREAMS]), "bounded": true};
}
export { computeKaalkaHashPayload, decryptSessionState, encryptSessionState, normalizeStreamEvents };
