/**
 * Converted from Python: core/streaming/live_update_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { makeStreamEvent } from "./streamCaptureEngine.js";

export let MAX_UPDATES: any = 5000;
export function trackLiveRuntimeUpdates(page: any): any {
  var updates: any[] = [];
  var events: any[] = [];
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("_test_live_updates") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_live_updates")] === "function")))) {
    updates = py.slice([...py.iter(page._test_live_updates)], null, MAX_UPDATES);
  }
  var index: any;
  var update: any;
  for ([index, update] of py.enumerate(updates)) {
    py.listAppend(events, makeStreamEvent(index, "live_update", py.toStr(py.get(update, "kind", "refresh")), py.toStr(py.get(update, "payload", "")), py.toStr(py.get(update, "target", ""))));
  }
  return {"updates": updates, "events": events, "bounded": true};
}
export { makeStreamEvent };
