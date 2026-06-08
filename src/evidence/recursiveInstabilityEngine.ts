/**
 * Converted from Python: core/evidence/recursive_instability_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelRecursiveInstability(unstable_regions: any, depth: any, evidence_count: any): any {
  var regions: any = [...py.iter(unstable_regions)];
  if ((depth > 2)) {
    py.listAppend(regions, `recursive:depth_${py.toStr(depth)}_instability`);
  }
  if ((evidence_count < 2)) {
    py.listAppend(regions, "recursive:weak_evidence");
  }
  return {"preserved": true, "unstable": py.truthy(regions), "regions": py.sorted(py.toSet(regions)), "depth": depth};
}
