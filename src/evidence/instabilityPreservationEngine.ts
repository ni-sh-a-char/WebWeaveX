/**
 * Converted from Python: core/evidence/instability_preservation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function preserveInstability(unstable_regions: any, evidence: any, stabilization_suppressed: any): any {
  var regions: any = [...py.iter(unstable_regions)];
  if ((py.len(evidence) < 2)) {
    py.listAppend(regions, "semantic:weak_evidence_instability");
  }
  if (py.truthy(stabilization_suppressed)) {
    py.listAppend(regions, "semantic:stabilization_blocked");
  }
  return {"preserved": true, "unstable": py.truthy(regions), "regions": py.sorted(py.toSet(regions)), "do_not_stabilize": true};
}
