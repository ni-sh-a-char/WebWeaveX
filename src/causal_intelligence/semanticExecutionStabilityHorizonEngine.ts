/**
 * Converted from Python: core/causal_intelligence/semantic_execution_stability_horizon_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function forecastStabilityHorizon(runtime_ir: any): any {
  var instability: any = py.get(runtime_ir, "instability_forecast", {});
  if (((instability !== null && typeof instability === "object" && !Array.isArray(instability) && !(instability instanceof Set) && !(instability instanceof Map)))) {
    var level: any = py.get(instability, "instability_forecast", "low");
  } else {
    level = "low";
  }
  var horizon: any = (py.eq(level, "high") ? "short" : "long");
  return {"stability_horizon": horizon, "instability_level": level};
}
