/**
 * Converted from Python: core/evidence/semantic_instability_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelSemanticInstability(unstable_regions: any, entropy: any, evidence: any): any {
  var regions: any = [...py.iter(unstable_regions)];
  if ((py.get(entropy, "entropy", 0) >= py.F(0.2))) {
    py.listAppend(regions, "semantic:entropy_instability");
  }
  return {"unstable": py.or2(py.truthy(regions), () => ((py.len(evidence) < 2))), "regions": py.sorted(py.toSet(regions)), "truth_pressure": py.round(py.add(py.get(entropy, "entropy", 0), ((py.len(evidence) < 2) ? py.F(0.3) : 0)), 3), "preserved": true};
}
