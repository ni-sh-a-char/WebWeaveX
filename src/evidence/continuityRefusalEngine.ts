/**
 * Converted from Python: core/evidence/continuity_refusal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function refuseUnsupportedContinuity(unsupported_continuity: any): any {
  var refusals: any = py.iter(unsupported_continuity).map((r: any) => ({"target": py.get(r, "reason", "continuity"), "message": "continuity_refused"}));
  return {"continuity_refusals": refusals, "termination_reasons": py.sorted(py.toSet(py.iter(refusals).map((r: any) => py.at(r, "message")))), "boundary_failures": py.iter(unsupported_continuity).map((r: any) => py.get(r, "reason"))};
}
