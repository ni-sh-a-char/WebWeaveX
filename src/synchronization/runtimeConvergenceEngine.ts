/**
 * Converted from Python: core/synchronization/runtime_convergence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function convergeRuntimeState(realities: any): any {
  var merged: Record<string, any> = {};
  var histories: any[] = [];
  var index: any;
  var reality: any;
  for ([index, reality] of py.enumerate(py.sorted(realities, {key: ((item: any) => py.toStr(py.get(item, "reality_id", ""))) as (item: any) => any}))) {
    var reality_id: any = py.toStr(py.get(reality, "reality_id", `reality:${py.toStr(index)}`));
    py.listAppend(histories, reality_id);
    var key: any;
    var value: any;
    for ([key, value] of py.items(reality)) {
      if (py.eq(key, "reality_id")) {
        continue;
      }
      if (!py.contains(merged, key)) {
        py.setItem(merged, key, value);
      } else if (!py.eq(py.at(merged, key), value)) {
        py.setItem(merged, key, value);
      }
    }
  }
  return {"converged_state": merged, "reality_count": py.len(realities), "histories": histories, "converged": true, "bounded": true};
}
