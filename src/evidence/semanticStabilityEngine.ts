/**
 * Converted from Python: core/evidence/semantic_stability_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelSemanticStability(evidence: any, drift_pressure: any, unsupported_continuity: any, parser_grounded: any): any {
  var unstable: any[] = [];
  if ((drift_pressure >= py.F(0.2))) {
    py.listAppend(unstable, "semantic:drift");
  }
  if (py.truthy(unsupported_continuity)) {
    py.listAppend(unstable, "semantic:continuity");
  }
  if (!py.truthy(parser_grounded)) {
    py.listAppend(unstable, "semantic:parser_gap");
  }
  if ((py.len(evidence) < 2)) {
    py.listAppend(unstable, "semantic:insufficient_evidence");
  }
  var stable: any = !py.truthy(unstable);
  return {"stable": stable, "level": (py.truthy(stable) ? "high" : ((py.len(unstable) >= 2) ? "low" : "medium")), "unstable_regions": py.sorted(py.toSet(unstable)), "boundary_pressure": py.round(py.min([py.F(1.0), py.mul(py.len(unstable), py.F(0.25))]), 3), "stability_limits": {"max_confidence": (!py.truthy(stable) ? py.F(0.5) : py.F(0.85))}};
}
