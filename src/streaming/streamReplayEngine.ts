/**
 * Converted from Python: core/streaming/stream_replay_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_REPLAY_EVENTS: any = 10000;
export function replayStreamEvents(page: any, stream_log: any): any {
  var replayed: any[] = [];
  var index: any;
  var event: any;
  for ([index, event] of py.enumerate(py.slice(stream_log, null, MAX_REPLAY_EVENTS))) {
    if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("_test_replay_log") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_replay_log")] === "function")))) {
      py.listAppend(page._test_replay_log, py.pyDict(event));
    }
    py.listAppend(replayed, {"step": index, "event": py.pyDict(event), "replayed": true});
  }
  return {"replay": replayed, "bounded": true};
}
export function buildStreamTimeline(events: any): any {
  var ordered: any = py.sorted([...py.iter(events)], {key: ((item: any) => [py.toInt(py.get(item, "timestamp", 0)), py.toStr(py.get(item, "id", "")), py.toStr(py.get(item, "source", ""))]) as (item: any) => any});
  var edges: any[] = [];
  var previous_id: any = "";
  var event: any;
  for (event of py.iter(ordered)) {
    var event_id: any = py.toStr(py.get(event, "id", ""));
    if (py.truthy(previous_id)) {
      py.listAppend(edges, {"from": previous_id, "to": event_id, "relation": "stream_next"});
    }
    previous_id = event_id;
  }
  return {"events": ordered, "edges": edges, "bounded": true};
}
