/**
 * Converted from Python: core/evidence/semantic_governance_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function suppressSemanticGovernance(governance_detected: any, depth: any): any {
  return {"governance": py.and2(governance_detected, () => ((depth >= 2))), "suppress": true, "centralized_governance_blocked": true};
}
