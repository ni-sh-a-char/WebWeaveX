/**
 * Converted from Python: core/crdt/semantic_crdt_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function mergeSemanticStates(left: any, right: any): any {
  var merged: any = py.pyDict(left);
  var key: any;
  var value: any;
  for ([key, value] of py.items(right)) {
    if (!py.contains(merged, key)) {
      py.setItem(merged, key, value);
      continue;
    }
    if (!py.eq(py.at(merged, key), value)) {
      py.setItem(merged, key, py.sorted([py.at(merged, key), value]));
    }
  }
  return {"state": merged, "merged": true};
}
