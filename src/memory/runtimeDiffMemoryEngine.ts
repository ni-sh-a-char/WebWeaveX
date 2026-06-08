/**
 * Converted from Python: core/memory/runtime_diff_memory_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function diffRuntimeMemory(previous: any, current: any): any {
  var prev_ids: any = py.toSet(py.iter(py.get(previous, "lineage", [])).map((item: any) => py.toStr(py.get(item, "id", ""))));
  var curr_ids: any = py.toSet(py.iter(py.get(current, "lineage", [])).map((item: any) => py.toStr(py.get(item, "id", ""))));
  return {"memory_changed": !py.eq(py.get(previous, "memory_id"), py.get(current, "memory_id")), "lineage_added": py.sorted(py.sub(curr_ids, prev_ids)), "lineage_removed": py.sorted(py.sub(prev_ids, curr_ids)), "history_delta": py.sub(py.len(py.get(current, "runtime_history", [])), py.len(py.get(previous, "runtime_history", []))), "revertible": true, "bounded": true};
}
