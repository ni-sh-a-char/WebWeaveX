/**
 * Converted from Python: core/evidence/recursive_phase_space_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelRecursivePhaseSpace(key_count: any, ambiguity_count: any, depth: any): any {
  var volume: any = py.round(py.min([py.F(1.0), py.add(py.mul(key_count, py.F(0.1)), py.mul(ambiguity_count, py.F(0.08)))]), 3);
  var reduction: any = py.and2((depth >= 4), () => ((key_count <= 1)));
  return {"volume": volume, "reduction_blocked": reduction, "preserved": (volume > 0)};
}
