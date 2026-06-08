/**
 * Converted from Python: core/evidence/semantic_termination_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function terminateSemanticChain(unstable_regions: any, continuity_refusals: any): any {
  var terminated: any = py.add([...py.iter(unstable_regions)], py.iter(continuity_refusals).map((r: any) => py.get(r, "target", "")));
  return {"terminated": py.sorted(py.toSet(py.iter(terminated).filter((t: any) => py.truthy(t)).map((t: any) => t))), "chain_stopped": py.truthy(terminated)};
}
