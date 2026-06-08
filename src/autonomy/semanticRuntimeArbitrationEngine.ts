/**
 * Converted from Python: core/autonomy/semantic_runtime_arbitration_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function arbitrateSemanticRuntime(runtimes: any): any {
  var ordered: any = py.sorted(runtimes, {key: ((x: any) => [py.toInt(py.get(x, "priority", 0)), py.toStr(py.get(x, "id"))]) as (item: any) => any});
  var chosen: any = (py.truthy(ordered) ? py.at(ordered, 0) : {});
  return {"selected_runtime": chosen, "runtime_count": py.len(ordered)};
}
