/**
 * Converted from Python: core/causal_intelligence/distributed_runtime_causal_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_GRAPH_EDGES: any = 100000;
export function buildDistributedCausalGraph(runtime_ir: any): any {
  var causality: any = py.get(runtime_ir, "runtime_causality_graph", {});
  var propagation: any = py.get(runtime_ir, "distributed_propagation", {});
  var causal_edges: any[] = [];
  var edge: any;
  for (edge of py.iter(py.slice(py.get(causality, "edges", []), null, MAX_GRAPH_EDGES))) {
    py.listAppend(causal_edges, {"from": py.get(edge, "from"), "to": py.get(edge, "to"), "relation": "execution_causes"});
  }
  var path: any;
  for (path of py.iter(py.slice(py.get(propagation, "propagation_paths", []), null, MAX_GRAPH_EDGES))) {
    py.listAppend(causal_edges, {"from": py.get(path, "source"), "to": py.get(path, "target"), "relation": "propagates"});
  }
  causal_edges = py.slice(py.sorted(causal_edges, {key: ((x: any) => [py.toStr(py.get(x, "from")), py.toStr(py.get(x, "to"))]) as (item: any) => any}), null, MAX_GRAPH_EDGES);
  return {"causal_edges": causal_edges, "edge_count": py.len(causal_edges), "bounded": true};
}
