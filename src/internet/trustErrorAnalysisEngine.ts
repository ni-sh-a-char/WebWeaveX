/**
 * Converted from Python: core/internet/trust_error_analysis_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function analyzeTrustError(predictions: any): any {
  var errors: any = py.iter(py.or2(predictions, () => ([]))).map((p: any) => py.pyAbs(py.sub(py.get(p, "predicted", 0), py.get(p, "actual", 0))));
  var mae: any = py.round(py.div(py.sum(errors), py.max([1, py.len(errors)])), 3);
  return {"mean_absolute_error": mae, "samples": py.len(errors), "calibration_error": mae, "deterministic_inputs": [`mae=${py.floatStr(mae)}`]};
}
