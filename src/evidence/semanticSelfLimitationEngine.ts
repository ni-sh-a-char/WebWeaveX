/**
 * Converted from Python: core/evidence/semantic_self_limitation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function applySemanticSelfLimitation(evidence: any, suppressed_speculation: any, noninferable_regions: any): any {
  var limited: any = py.or2((py.len(evidence) < 2), () => (py.or2(py.truthy(suppressed_speculation), () => (py.truthy(noninferable_regions)))));
  return {"active": limited, "prefer_cannot_determine": true, "propagation_allowed": !py.truthy(limited), "reconciliation_allowed": (py.len(evidence) >= 2), "expansion_allowed": py.and2((py.len(evidence) >= 2), () => (!py.truthy(noninferable_regions))), "limit_reasons": py.sorted(py.toSet(py.add(py.add(((py.len(evidence) < 2) ? ["insufficient_evidence"] : []), (py.truthy(suppressed_speculation) ? ["speculative_suppression"] : [])), (py.truthy(noninferable_regions) ? ["noninferable_regions"] : []))))};
}
