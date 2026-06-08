/**
 * Converted from Python: core/kernel/runtime_coordination.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function coordinateKernelPhases(phase_results: any, tick: any = 0): any {
  var ordered: any = py.sorted(phase_results, {key: ((item: any) => py.toStr(py.get(item, "phase", ""))) as (item: any) => any});
  return {"phases": ordered, "tick": tick, "coordinated": true, "bounded": true};
}
