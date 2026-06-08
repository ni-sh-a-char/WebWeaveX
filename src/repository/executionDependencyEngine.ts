/**
 * Converted from Python: core/repository/execution_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconstructExecutionFlow } from "./executionFlowEngine.js";
import { parseSource } from "../parsers/parserRegistry.js";

export function modelExecutionDependencies(source: any, path: any = ""): any {
  var parsed: any = (py.truthy(source) ? parseSource(source, path) : {});
  var flow: any = reconstructExecutionFlow(parsed);
  var edges: any[] = [];
  var prev: any = null;
  var step: any;
  for (step of py.iter(py.get(flow, "flow", []))) {
    var call: any = (((py.get(step, "call") !== null && typeof py.get(step, "call") === "object" && !Array.isArray(py.get(step, "call")) && !(py.get(step, "call") instanceof Set) && !(py.get(step, "call") instanceof Map))) ? py.get(step, "call", {}) : {});
    var cur: any = py.or2(py.get(call, "callee"), () => (py.or2(py.get(call, "caller"), () => (""))));
    if ((py.truthy(prev) && py.truthy(cur))) {
      py.listAppend(edges, {"from": py.toStr(prev), "to": py.toStr(cur), "evidence": ["parser:call_graph"]});
    }
    prev = py.or2(cur, () => (prev));
  }
  return {"edges": edges, "entrypoints": py.get(flow, "entrypoints", []), "evidence": py.get(flow, "evidence", [])};
}
export { parseSource, reconstructExecutionFlow };
