/**
 * Converted from Python: core/evidence/recursive_agency_decay_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resistAgencyDecay(agency_ok: any, depth: any): any {
  return {"decay_risk": py.and2((depth >= 4), () => (!py.truthy(agency_ok))), "resist": true, "erosion_suppressed": true};
}
