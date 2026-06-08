/**
 * Converted from Python: core/streaming/stream_capture_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_STREAM_EVENTS: any = 10000;
export function makeStreamEvent(step: any, source: any, direction: any, payload: any, connection_id: any): any {
  return {"id": `stream_${py.toStr(step)}`, "timestamp": step, "source": py.toStr(source), "direction": py.toStr(direction), "payload": py.slice(py.toStr(payload), null, 10000), "connection_id": py.toStr(connection_id), "bounded": true};
}
export function normalizeStreamEvents(events: any): any {
  var normalized: any[] = [];
  var index: any;
  var event: any;
  for ([index, event] of py.enumerate(py.slice(events, null, MAX_STREAM_EVENTS))) {
    py.listAppend(normalized, makeStreamEvent(py.toInt(py.get(event, "timestamp", index)), py.toStr(py.get(event, "source", "unknown")), py.toStr(py.get(event, "direction", "incoming")), py.toStr(py.get(event, "payload", "")), py.toStr(py.get(event, "connection_id", ""))));
  }
  return py.sorted(normalized, {key: ((item: any) => [py.toInt(py.get(item, "timestamp", 0)), py.toStr(py.get(item, "id", ""))]) as (item: any) => any});
}
