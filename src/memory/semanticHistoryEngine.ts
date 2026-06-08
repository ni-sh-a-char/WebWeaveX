/**
 * Converted from Python: core/memory/semantic_history_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function recordHistory(events: any, max_events: any = 500): any {
  var bounded: any = py.slice(events, (-max_events), null);
  return {"events": bounded, "count": py.len(bounded), "truncated": (py.len(events) > max_events)};
}
