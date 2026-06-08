/**
 * Converted from Python: core/evidence/noninferable_scope_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelNoninferableRegions(inferred: any, evidence: any, noninferences: any, min_evidence: any = 2): any {
  var regions: any = [...py.iter(noninferences)];
  if (((py.len(evidence) < min_evidence) && py.truthy(inferred))) {
    py.listAppend(regions, "semantic:insufficient_evidence");
  }
  if ((py.truthy(inferred) && !py.truthy(evidence))) {
    py.listAppend(regions, "semantic:ungrounded_inference");
  }
  var voids: any = py.sorted(py.toSet(regions));
  return {"noninferable_regions": voids, "inference_voids": voids, "semantic_boundaries": {"min_evidence": min_evidence, "blocked": (py.len(voids) > 0)}, "unsupported_scope": {"regions": voids, "count": py.len(voids)}, "epistemic_limits": {"cannot_determine": (py.len(voids) > 0), "reason": (py.truthy(voids) ? "insufficient_evidence" : null)}};
}
