/**
 * Converted from Python: core/evolution/semantic_repository_diff_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function diffSemanticRepository(left: any, right: any): any {
  var left_keys: any = py.toSet(py.keys(left));
  var right_keys: any = py.toSet(py.keys(right));
  return {"added": py.sorted(py.sub(right_keys, left_keys)), "removed": py.sorted(py.sub(left_keys, right_keys))};
}
