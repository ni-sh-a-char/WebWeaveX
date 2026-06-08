/**
 * Converted from Python: core/execution_reality/runtime_conflict_detection_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_CONFLICTS: any = 1000;
export function detectRuntimeConflicts(runtime_ir: any): any {
  var transitions: any = py.get(runtime_ir, "transitions", []);
  var seen: Set<any> = new Set();
  var conflicts: any[] = [];
  var transition: any;
  for (transition of py.iter(transitions)) {
    var key: any = [py.get(transition, "from"), py.get(transition, "to")];
    if (py.contains(seen, key)) {
      py.listAppend(conflicts, key);
    }
    py.setAdd(seen, key);
  }
  return {"conflicts": py.slice(py.sorted(conflicts, {key: ((x: any) => [py.toStr(py.at(x, 0)), py.toStr(py.at(x, 1))]) as (item: any) => any}), null, MAX_CONFLICTS)};
}
