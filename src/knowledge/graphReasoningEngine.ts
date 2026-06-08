/**
 * Converted from Python: core/knowledge/graph_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function reasonOverSemanticGraph(graph: any): any {
  var nodes: any = py.get(py.or2(graph, () => ({})), "nodes", []);
  var edges: any = py.get(py.or2(graph, () => ({})), "edges", []);
  var adjacency: Record<string, any> = {};
  var e: any;
  for (e of py.iter(edges)) {
    py.setdefault(adjacency, py.get(e, "from"), 0);
    py.setItem(adjacency, py.get(e, "from"), py.add(py.at(adjacency, py.get(e, "from")), 1));
  }
  var hubs: any = py.slice(py.sorted(py.items(adjacency), {key: ((kv: any) => [(-py.at(kv, 1)), py.at(kv, 0)]) as (item: any) => any}), null, 10);
  return {"node_count": py.len(nodes), "edge_count": py.len(edges), "connected": (py.len(edges) > 0), "hubs": py.iter(hubs).map(([n, d]: any) => ({"node": n, "out_degree": d}))};
}
