/**
 * Converted from Python: core/evidence/recursive_confidence_echo_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectRecursiveConfidenceEcho(score: any, depth: any, prior_scores: any): any {
  if (((depth < 2) || !py.truthy(prior_scores))) {
    return {"echo_detected": false, "suppress": false};
  }
  var avg: any = py.div(py.sum(prior_scores), py.len(prior_scores));
  var echo: any = (score > py.add(avg, py.mul(py.F(0.1), depth)));
  return {"echo_detected": echo, "suppress": echo, "decay_to": (py.truthy(echo) ? py.round(py.min([score, avg]), 3) : score)};
}
