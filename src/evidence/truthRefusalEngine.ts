/**
 * Converted from Python: core/evidence/truth_refusal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function refuseUnsupportedStabilization(suppressed: any): any {
  var refusals: any = py.iter(suppressed).map((s: any) => ({"target": py.get(s, "reason", "stabilization"), "message": "truthfully_incomplete"}));
  return {"truth_refusals": refusals, "stabilization_failures": py.iter(suppressed).map((s: any) => py.get(s, "reason")), "truth_boundary_failures": py.iter(suppressed).map((s: any) => py.get(py.get(s, "truth_boundary_violation", {}), "type")), "termination_reasons": py.sorted(py.toSet(py.iter(refusals).map((r: any) => py.at(r, "message"))))};
}
