/**
 * Converted from Python: core/evidence/semantic_decay_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelSemanticDecay(evidence: any, inferred: any, stabilization_count: any): any {
  var decay_rate: any = py.round(py.min([py.F(1.0), py.add(py.mul(py.div(py.len(inferred), py.max([1, py.add(py.len(evidence), 1)])), py.F(0.2)), py.mul(stabilization_count, py.F(0.15)))]), 3);
  return {"decaying": (decay_rate > 0), "decay_rate": decay_rate, "destabilize_unsupported": (py.len(evidence) < 2), "prefer_incomplete": true};
}
