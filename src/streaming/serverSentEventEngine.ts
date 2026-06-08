/**
 * Converted from Python: core/streaming/server_sent_event_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { makeStreamEvent, normalizeStreamEvents } from "./streamCaptureEngine.js";

export let MAX_SSE_EVENTS: any = 5000;
export function captureServerSentEvents(page: any): any {
  var events: any[] = [];
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("_test_sse_events") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_sse_events")] === "function")))) {
    var index: any;
    var item: any;
    for ([index, item] of py.enumerate(py.slice(page._test_sse_events, null, MAX_SSE_EVENTS))) {
      py.listAppend(events, makeStreamEvent(index, "sse", "incoming", py.toStr(py.get(item, "payload", "")), py.toStr(py.get(item, "event_type", "message"))));
    }
  }
  return {"events": normalizeStreamEvents(events), "bounded": true};
}
export { makeStreamEvent, normalizeStreamEvents };
