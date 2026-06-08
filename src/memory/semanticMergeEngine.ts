/**
 * Converted from Python: core/memory/semantic_merge_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function mergeSemanticStates(left: any, right: any): any {
  var merged: any = py.pyDict(left);
  var k: any;
  var v: any;
  for ([k, v] of py.iter(py.sorted(py.items(right)))) {
    if (!py.contains(merged, k)) {
      py.setItem(merged, k, v);
    } else if (!py.eq(py.at(merged, k), v)) {
      py.setItem(merged, k, {"left": py.at(merged, k), "right": v, "conflict": true});
    }
  }
  return {"state": merged, "deterministic": true};
}
