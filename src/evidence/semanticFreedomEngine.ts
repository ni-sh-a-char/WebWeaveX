/**
 * Converted from Python: core/evidence/semantic_freedom_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelSemanticFreedom(autonomy: any, competition: any): any {
  return {"free": py.and2(py.get(autonomy, "autonomous", true), () => (py.get(competition, "competitive", true))), "governance_suppressed": true, "hierarchy_permanence_blocked": true};
}
