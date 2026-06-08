/**
 * Converted from Python: core/execution_reality/distributed_runtime_stability_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_STABLE_PRESSURE: any = 50000;
export function assessDistributedStability(runtime_ir: any): any {
  var pressure: any = py.get(runtime_ir, "execution_pressure", {});
  var score: any = py.toInt(py.get(pressure, "pressure_score", 0));
  return {"stable": py.lt(score, MAX_STABLE_PRESSURE), "pressure_score": score};
}
