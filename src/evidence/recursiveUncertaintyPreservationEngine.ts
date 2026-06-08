/**
 * Converted from Python: core/evidence/recursive_uncertainty_preservation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function preserveRecursiveUncertainty(uncertainties: any, depth: any): any {
  return {"preserved": true, "items": py.sorted(py.toSet(py.iter(uncertainties).map((u: any) => py.toStr(u)))), "depth": depth, "collapse_suppressed": true};
}
