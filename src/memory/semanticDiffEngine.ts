/**
 * Converted from Python: core/memory/semantic_diff_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function diffSemanticIr(before: any, after: any): any {
  var changes: any[] = [];
  var key: any;
  for (key of py.iter(py.sorted(py.bitor(py.toSet(py.keys(before)), py.toSet(py.keys(after)))))) {
    if (!py.eq(py.get(before, key), py.get(after, key))) {
      py.listAppend(changes, {"field": key, "changed": "true"});
    }
  }
  return {"changes": changes, "change_count": py.len(changes), "deterministic": true};
}
