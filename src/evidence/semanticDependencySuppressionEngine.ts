/**
 * Converted from Python: core/evidence/semantic_dependency_suppression_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function suppressSemanticDependency(suppressed: any): any {
  return {"suppressed": py.len(suppressed), "active": py.truthy(suppressed), "loops_blocked": true};
}
