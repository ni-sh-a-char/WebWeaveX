/**
 * Converted from Python: core/runtime/event_stream_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export let MAX_EVENT_CHAIN: any = 1000;
export function reconstructEventStream(events: any): any {
  var ordered: any = py.sorted(py.slice(events, null, MAX_EVENT_CHAIN), {key: ((x: any) => py.get(x, "timestamp", 0)) as (item: any) => any});
  var edges: any[] = [];
  var i: any;
  for (i = 0; i < py.sub(py.len(ordered), 1); i++) {
    py.listAppend(edges, {"from": py.get(py.at(ordered, i), "id"), "to": py.get(py.at(ordered, py.add(i, 1)), "id"), "relation": "event_precedes"});
  }
  return {"events": ordered, "edges": edges, "bounded": true};
}
