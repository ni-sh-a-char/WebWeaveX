/**
 * Converted from Python: core/evidence/inference_termination_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function terminateInferenceChain(refused_inferences: any, suppressed_speculation: any): any {
  var terminated: any = py.add([...py.iter(refused_inferences)], py.iter(suppressed_speculation).filter((s: any) => ((s !== null && typeof s === "object" && !Array.isArray(s) && !(s instanceof Set) && !(s instanceof Map)))).map((s: any) => py.get(s, "reason", "speculative")));
  return {"terminated_inferences": py.sorted(py.toSet(terminated)), "chain_stopped": py.truthy(terminated), "stop_at": (py.truthy(terminated) ? py.at(terminated, 0) : null)};
}
