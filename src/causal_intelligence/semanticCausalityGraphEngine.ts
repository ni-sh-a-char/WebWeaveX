/**
 * Converted from Python: core/causal_intelligence/semantic_causality_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_CAUSAL_EDGES: any = 100000;
export function buildSemanticCausalityGraph(runtime_ir: any): any {
  var transitions: any = [...py.iter(py.get(runtime_ir, "transitions", []))];
  var edges: any[] = [];
  var transition: any;
  for (transition of py.iter(py.slice(transitions, null, MAX_CAUSAL_EDGES))) {
    var source: any = py.toStr(py.get(transition, "from", "unknown"));
    var target: any = py.toStr(py.get(transition, "to", "unknown"));
    py.listAppend(edges, {"from": source, "to": target, "relation": "causes"});
  }
  var node_set: any = py.union(py.toSet(py.iter(edges).map((edge: any) => py.at(edge, "from"))), py.toSet(py.iter(edges).map((edge: any) => py.at(edge, "to"))));
  return {"nodes": py.slice(py.sorted(node_set), null, MAX_CAUSAL_EDGES), "edges": py.slice(py.sorted(edges, {key: ((x: any) => [py.at(x, "from"), py.at(x, "to")]) as (item: any) => any}), null, MAX_CAUSAL_EDGES), "bounded": true};
}
