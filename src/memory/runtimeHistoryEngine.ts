/**
 * Converted from Python: core/memory/runtime_history_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function appendRuntimeHistory(history: any, entry: any): any {
  var updated: any = [...py.iter(history)];
  py.listAppend(updated, entry);
  return py.slice(py.sorted(updated, {key: ((item: any) => py.toInt(py.get(item, "tick", 0))) as (item: any) => any}), null, 100000);
}
