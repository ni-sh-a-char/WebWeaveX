/**
 * Converted from Python: core/streaming/websocket_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { makeStreamEvent, normalizeStreamEvents } from "./streamCaptureEngine.js";

export let MAX_FRAMES: any = 10000;
export let MAX_CONNECTIONS: any = 1000;
export function trackWebsocketConnections(page: any): any {
  var connections: any[] = [];
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("_test_websocket_connections") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_websocket_connections")] === "function")))) {
    connections = py.slice([...py.iter(page._test_websocket_connections)], null, MAX_CONNECTIONS);
  } else if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("_test_websocket_frames") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_websocket_frames")] === "function")))) {
    var seen: Record<string, any> = {};
    var frame: any;
    for (frame of py.iter(py.slice(page._test_websocket_frames, null, MAX_CONNECTIONS))) {
      var connection_id: any = py.toStr(py.get(frame, "connection_id", ""));
      if (!py.contains(seen, connection_id)) {
        py.setItem(seen, connection_id, {"connection_id": connection_id, "url": py.slice(py.toStr(py.get(frame, "url", "")), null, 2000), "lifecycle": "open"});
      }
    }
    connections = py.sorted(py.values(seen), {key: ((item: any) => py.toStr(py.get(item, "connection_id", ""))) as (item: any) => any});
  }
  return {"connections": connections, "bounded": true};
}
export function captureWebsocketFrames(page: any): any {
  var events: any[] = [];
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("_test_websocket_frames") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_websocket_frames")] === "function")))) {
    var index: any;
    var frame: any;
    for ([index, frame] of py.enumerate(py.slice(page._test_websocket_frames, null, MAX_FRAMES))) {
      py.listAppend(events, makeStreamEvent(index, "websocket", py.toStr(py.get(frame, "direction", "incoming")), py.toStr(py.get(frame, "payload", "")), py.toStr(py.get(frame, "connection_id", ""))));
    }
  }
  return {"events": normalizeStreamEvents(events), "bounded": true};
}
export { makeStreamEvent, normalizeStreamEvents };
