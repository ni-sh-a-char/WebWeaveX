/**
 * Converted from Python: core/evidence/recursive_self_confirmation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectRecursiveSelfConfirmation(depth: any, reconciled_eq_inferred: any, evidence_count: any): any {
  var confirm: any = py.and2((depth >= 2), () => (py.and2(reconciled_eq_inferred, () => ((evidence_count < 2)))));
  return {"detected": confirm, "suppress": confirm, "recursive_pressure": (py.truthy(confirm) ? py.round(py.mul(depth, py.F(0.1)), 3) : py.F(0.0))};
}
