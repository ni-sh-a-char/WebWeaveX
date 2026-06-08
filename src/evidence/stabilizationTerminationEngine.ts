/**
 * Converted from Python: core/evidence/stabilization_termination_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function terminateStabilization(suppressed: any, unstable_regions: any): any {
  var terminated: any = py.add(py.iter(suppressed).map((s: any) => py.get(s, "reason", "")), unstable_regions);
  return {"terminated": py.sorted(py.toSet(py.iter(terminated).filter((t: any) => py.truthy(t)).map((t: any) => t))), "chain_stopped": py.truthy(terminated)};
}
