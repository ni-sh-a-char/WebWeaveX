/**
 * Converted from Python: core/kernel/runtime_topology.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildKernelTopology(graph: any = null): any {
  graph = py.or2(graph, () => ({}));
  var nodes: any = py.sorted(py.get(graph, "nodes", []), {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any});
  var edges: any = py.sorted(py.get(graph, "edges", []), {key: ((item: any) => [py.toStr(py.get(item, "from", "")), py.toStr(py.get(item, "to", "")), py.toStr(py.get(item, "relation", ""))]) as (item: any) => any});
  return {"nodes": nodes, "edges": edges, "node_count": py.len(nodes), "bounded": true};
}
