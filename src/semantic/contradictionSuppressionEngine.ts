/**
 * Converted from Python: core/semantic/contradiction_suppression_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function suppressUnderContradiction(expansions: any, contradiction_pressure: any): any {
  if (!py.truthy(py.get(contradiction_pressure, "suppress_propagation"))) {
    return {"suppressed": [], "allowed": expansions};
  }
  return {"suppressed": py.sorted(expansions), "allowed": [], "reason": "contradiction_pressure"};
}
