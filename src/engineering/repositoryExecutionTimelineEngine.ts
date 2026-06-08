/**
 * Converted from Python: core/engineering/repository_execution_timeline_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_TIMELINE: any = 10000;
export function buildExecutionTimeline(events: any): any {
  var ordered: any = py.slice(py.sorted(events, {key: ((x: any) => [py.get(x, "timestamp", 0), py.toStr(py.get(x, "id"))]) as (item: any) => any}), null, MAX_TIMELINE);
  return {"timeline": ordered, "timeline_size": py.len(ordered), "bounded": true};
}
