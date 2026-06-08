/**
 * Converted from Python: core/internet/trust_calibration_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeTrust } from "./trustEngine.js";

export function calibrateTrust(url: any, corroboration_count: any = 0, html_text: any = "", claims: any = null): any {
  var base: any = computeTrust(url, corroboration_count, html_text, claims);
  var evidence: any = py.or2(py.get(base, "evidence", []), () => ([]));
  var density: any = py.round(py.min([py.F(1.0), py.mul(py.len(evidence), py.F(0.1))]), 3);
  var calibration_error: any = py.round(py.pyAbs(py.sub(py.get(base, "trust_score", 0), density)), 3);
  return {...(base), "calibrated": true, "evidence_density": density, "calibration_error": calibration_error, "opaque_heuristic": false, "deterministic_inputs": py.sorted(py.toSet(py.add([...py.iter(py.get(base, "deterministic_inputs", []))], [`density=${py.floatStr(density)}`, `cal_err=${py.floatStr(calibration_error)}`])))};
}
export { computeTrust };
