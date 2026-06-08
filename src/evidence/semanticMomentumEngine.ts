/**
 * Converted from Python: core/evidence/semantic_momentum_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function measureSemanticMomentum(inferred_count: any, evidence_count: any): any {
  var ratio: any = py.div(inferred_count, py.max([1, evidence_count]));
  var pressure: any = py.round(py.min([py.F(1.0), py.mul(py.max([py.F(0.0), py.sub(ratio, py.F(1.0))]), py.F(0.3))]), 3);
  return {"momentum": pressure, "halt_expansion": (pressure >= py.F(0.25)), "inferred_count": inferred_count, "evidence_count": evidence_count};
}
