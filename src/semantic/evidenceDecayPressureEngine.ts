/**
 * Converted from Python: core/semantic/evidence_decay_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeEvidenceDecayPressure(evidence_count: any, min_evidence: any = 2): any {
  var gap: any = py.max([0, py.sub(min_evidence, evidence_count)]);
  return {"pressure": py.round(py.min([py.F(1.0), py.mul(gap, py.F(0.4))]), 3), "incomplete": (gap > 0)};
}
