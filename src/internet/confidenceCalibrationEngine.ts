/**
 * Converted from Python: core/internet/confidence_calibration_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function calibrateConfidence(predicted: any, observed_accuracy: any): any {
  var error: any = py.round(py.pyAbs(py.sub(predicted, observed_accuracy)), 3);
  var reliable: any = (error < py.F(0.25));
  return {"predicted": py.round(predicted, 3), "observed_accuracy": py.round(observed_accuracy, 3), "calibration_error": error, "reliable": reliable, "deterministic_inputs": [`error=${py.floatStr(error)}`]};
}
