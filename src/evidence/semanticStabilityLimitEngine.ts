/**
 * Converted from Python: core/evidence/semantic_stability_limit_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function semanticStabilityLimits(stability: any): any {
  return {"max_confidence": py.get(py.get(stability, "stability_limits", {}), "max_confidence", py.F(0.5)), "expansion_allowed": py.get(stability, "stable", false)};
}
