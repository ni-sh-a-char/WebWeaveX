/**
 * Converted from Python: core/causality/runtime_timeline_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeTimeline(events: any, propagation: any): any {
  var ordered: any = py.sorted(events, {key: ((item: any) => py.toInt(py.get(item, "step", 0))) as (item: any) => any});
  var timeline: any[] = [];
  var index: any;
  var event: any;
  for ([index, event] of py.enumerate(py.slice(ordered, null, 10000))) {
    py.listAppend(timeline, {"step": index, "event_id": py.toStr(py.get(event, "id", `evt:${py.toStr(index)}`)), "runtime": py.toStr(py.get(event, "runtime", "")), "type": py.toStr(py.get(event, "type", "mutation")), "propagation_map": py.iter(py.get(propagation, "handoffs", [])).filter((handoff: any) => py.eq(py.get(handoff, "step"), index)).map((handoff: any) => py.get(handoff, "workflow_id", ""))});
  }
  return {"timeline": timeline, "evolution_history": py.iter(timeline).map((entry: any) => py.at(entry, "event_id")), "propagation_maps": [...py.iter(py.get(propagation, "handoffs", []))], "bounded": true};
}
