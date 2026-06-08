/**
 * Converted from Python: core/synchronization/runtime_timeline_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildSyncTimeline(history: any): any {
  var entries: any[] = [];
  var delta: any;
  for (delta of py.iter(py.get(history, "deltas", []))) {
    py.listAppend(entries, {"tick": py.toInt(py.get(delta, "timestamp", 0)), "delta_id": py.toStr(py.get(delta, "delta_id", "")), "change_count": py.len(py.get(delta, "changes", []))});
  }
  return {"timeline": py.sorted(entries, {key: ((item: any) => py.at(item, "tick")) as (item: any) => any}), "bounded": true};
}
