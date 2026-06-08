/**
 * Converted from Python: core/internet/probabilistic_trust_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { calibrateTrust } from "./trustCalibrationEngine.js";

export function computeProbabilisticTrust(url: any, corroboration_count: any = 0, html_text: any = "", claims: any = null): any {
  var base: any = calibrateTrust(url, corroboration_count, html_text, claims);
  var density: any = py.get(base, "evidence_density", 0);
  var score: any = py.get(base, "trust_score", 0);
  var posterior: any = py.round(py.min([py.F(1.0), py.add(py.mul(score, py.F(0.7)), py.mul(density, py.F(0.3)))]), 3);
  return {...(base), "trust_score": posterior, "score": posterior, "posterior": posterior, "prior": score, "calibrated": true, "deterministic_inputs": py.sorted(py.toSet(py.add([...py.iter(py.get(base, "deterministic_inputs", []))], [`posterior=${py.floatStr(posterior)}`])))};
}
export { calibrateTrust };
