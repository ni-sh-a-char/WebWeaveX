/**
 * Converted from Python: core/causality/causal_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildCausalGraph(events: any, causality: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var seen_runtimes: Set<any> = new Set();
  var event: any;
  for (event of py.iter(py.slice(events, null, 10000))) {
    var event_id: any = py.toStr(py.get(event, "id", ""));
    py.listAppend(nodes, {"id": event_id, "type": "event", "runtime": py.toStr(py.get(event, "runtime", ""))});
    var runtime: any = py.toStr(py.get(event, "runtime", ""));
    if ((py.truthy(runtime) && !py.contains(seen_runtimes, runtime))) {
      py.setAdd(seen_runtimes, runtime);
      py.listAppend(nodes, {"id": `runtime:${py.toStr(runtime)}`, "type": "runtime"});
      py.listAppend(edges, {"from": `runtime:${py.toStr(runtime)}`, "to": event_id, "relation": "triggers"});
    }
  }
  var edge: any;
  for (edge of py.iter(py.slice(py.get(causality, "causal_edges", []), null, 10000))) {
    py.listAppend(edges, {"from": py.toStr(py.get(edge, "from", "")), "to": py.toStr(py.get(edge, "to", "")), "relation": "propagates"});
  }
  var index: any;
  for ([index, event] of py.enumerate(py.slice(events, null, 10000))) {
    if (py.eq(py.get(event, "type"), "notification")) {
      event_id = py.toStr(py.get(event, "id", `evt:${py.toStr(index)}`));
      py.listAppend(edges, {"from": event_id, "to": `workflow:${py.toStr(index)}`, "relation": "mutates"});
    }
  }
  if (!py.truthy(nodes)) {
    py.listAppend(nodes, {"id": "causality:root", "type": "causality"});
  }
  return {"nodes": py.sorted(nodes, {key: ((item: any) => py.at(item, "id")) as (item: any) => any}), "edges": py.sorted(edges, {key: ((item: any) => [py.get(item, "from", ""), py.get(item, "to", ""), py.get(item, "relation", "")]) as (item: any) => any}), "bounded": true};
}
