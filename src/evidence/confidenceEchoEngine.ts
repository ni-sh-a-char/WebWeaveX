/**
 * Converted from Python: core/evidence/confidence_echo_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectConfidenceEcho(score: any, prior_scores: any): any {
  if (!py.truthy(prior_scores)) {
    return {"echo_detected": false, "suppress": false};
  }
  var avg_prior: any = py.div(py.sum(prior_scores), py.len(prior_scores));
  var echo: any = py.and2((score > py.add(avg_prior, py.F(0.15))), () => ((score > py.F(0.6))));
  return {"echo_detected": echo, "suppress": echo, "collapse_to": (py.truthy(echo) ? py.round(py.min([score, avg_prior]), 3) : score)};
}
