/**
 * Converted from Python: core/repository/repository_execution_flow_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_FLOWS: any = 10000;
export function reconstructExecutionFlows(dependencies: any): any {
  var flows: any[] = [];
  var edge: any;
  for (edge of py.iter(py.get(dependencies, "edges", []))) {
    py.listAppend(flows, {"from": py.get(edge, "from"), "to": py.get(edge, "to"), "relation": py.get(edge, "relation", "imports")});
  }
  var dep: any;
  for (dep of py.iter(py.get(dependencies, "imports", []))) {
    py.listAppend(flows, {"from": "module", "to": dep, "relation": "imports"});
    if ((py.len(flows) >= MAX_FLOWS)) {
      break;
    }
  }
  return {"flows": py.slice(py.sorted(flows, {key: ((x: any) => [py.toStr(py.get(x, "from")), py.toStr(py.get(x, "to"))]) as (item: any) => any}), null, MAX_FLOWS), "bounded": true};
}
