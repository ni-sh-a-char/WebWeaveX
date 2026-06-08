/**
 * Converted from Python: core/semantic/evidence_boundary_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeEvidenceBoundaryPressure(evidence_count: any, min_evidence: any = 2): any {
  var gap: any = py.max([0, py.sub(min_evidence, evidence_count)]);
  var pressure: any = py.round(py.min([py.F(1.0), py.mul(gap, py.F(0.35))]), 3);
  return {"pressure": pressure, "violation": (gap > 0), "gap": gap};
}
