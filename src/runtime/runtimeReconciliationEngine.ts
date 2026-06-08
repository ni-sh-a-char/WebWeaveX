/**
 * Converted from Python: core/runtime/runtime_reconciliation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function reconcileRuntimeStates(left: any, right: any): any {
  var left_keys: any = py.toSet(py.keys(left));
  var right_keys: any = py.toSet(py.keys(right));
  var only_left: any = py.sorted(py.sub(left_keys, right_keys));
  var only_right: any = py.sorted(py.sub(right_keys, left_keys));
  var shared: any = py.sorted(py.bitand(left_keys, right_keys));
  var conflicts: any = py.sorted(py.iter(shared).filter((k: any) => !py.eq(py.get(left, k), py.get(right, k))).map((k: any) => k));
  return {"only_left": only_left, "only_right": only_right, "conflicts": conflicts, "aligned": py.sorted(py.iter(shared).filter((k: any) => !py.contains(conflicts, k)).map((k: any) => k)), "deterministic": true};
}
