/**
 * Converted from Python: core/causal_intelligence/semantic_instability_forecast_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let INSTABILITY_PRESSURE_THRESHOLD: any = 5000;
export function forecastRuntimeInstability(runtime_ir: any): any {
  var pressure: any = py.get(runtime_ir, "execution_pressure", {});
  var score: any = py.toInt(py.get(pressure, "pressure_score", 0));
  var instability: any = (py.gt(score, INSTABILITY_PRESSURE_THRESHOLD) ? "high" : "low");
  return {"instability_forecast": instability, "pressure_score": score};
}
