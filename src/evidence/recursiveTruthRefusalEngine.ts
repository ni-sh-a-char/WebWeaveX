/**
 * Converted from Python: core/evidence/recursive_truth_refusal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function refuseRecursiveStabilization(suppressed: any): any {
  var refusals: any = py.iter(suppressed).map((s: any) => ({"target": py.get(s, "reason", "closure"), "message": "recursive_truthfully_incomplete"}));
  return {"recursive_truth_refusals": refusals, "recursive_stabilization_failures": py.iter(suppressed).map((s: any) => py.get(s, "reason")), "recursive_boundary_failures": py.iter(suppressed).map((s: any) => py.get(py.get(s, "truth_boundary_violation", {}), "type")), "recursive_termination_reasons": py.sorted(py.toSet(py.iter(refusals).map((r: any) => py.at(r, "message"))))};
}
