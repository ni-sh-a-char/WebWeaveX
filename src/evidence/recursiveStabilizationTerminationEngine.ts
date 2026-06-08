/**
 * Converted from Python: core/evidence/recursive_stabilization_termination_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function terminateRecursiveStabilization(suppressed: any, depth: any): any {
  var terminated: any = py.add(py.iter(suppressed).map((s: any) => py.get(s, "reason", "")), ((depth >= 4) ? [`depth_${py.toStr(depth)}_limit`] : []));
  return {"terminated": py.sorted(py.toSet(py.iter(terminated).filter((t: any) => py.truthy(t)).map((t: any) => t))), "chain_stopped": py.truthy(terminated)};
}
