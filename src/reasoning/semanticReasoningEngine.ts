/**
 * Converted from Python: core/reasoning/semantic_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reasonRuntimeSemantic } from "./runtimeReasoningEngine.js";
import { reasonDiscourseSemantic } from "./discourseReasoningEngine.js";
import { reasonTopologySemantic } from "./topologyReasoningEngine.js";

export function reasonSemantically(domain: any, payload: any): any {
  var dispatch: any = {"runtime": () => reasonRuntimeSemantic(py.get(payload, "source", ""), py.get(payload, "path", "")), "discourse": () => reasonDiscourseSemantic(py.get(payload, "text", "")), "topology": () => reasonTopologySemantic(py.get(payload, "graph", {}))};
  var fn: any = py.get(dispatch, domain);
  if (!py.truthy(fn)) {
    return {"error": "unknown_domain", "explainable": true};
  }
  var result: any = fn();
  return {...(result), "domain": domain, "deterministic": true};
}
export { reasonDiscourseSemantic, reasonRuntimeSemantic, reasonTopologySemantic };
