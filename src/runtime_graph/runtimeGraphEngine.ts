/**
 * Converted from Python: core/runtime_graph/runtime_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_GRAPH_NODES: any = 1000000;
export let MAX_GRAPH_EDGES: any = 5000000;
export function buildRuntimeGraph(runtime_irs: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var seen_nodes: Set<any> = new Set();
  var seen_edges: Set<any> = new Set();
  var runtime: any;
  for (runtime of py.iter(py.slice(runtime_irs, null, 10000))) {
    var runtime_type: any = py.toStr(py.get(runtime, "ir", "unknown"));
    var runtime_nodes: any = [...py.iter(py.or2(py.get(runtime, "nodes", []), () => ([])))];
    var runtime_edges: any = [...py.iter(py.or2(py.get(runtime, "edges", []), () => ([])))];
    var node: any;
    for (node of py.iter(runtime_nodes)) {
      var node_id: any = py.strip(py.toStr(py.get(node, "id", "")));
      if (!py.truthy(node_id)) {
        continue;
      }
      if (py.contains(seen_nodes, node_id)) {
        continue;
      }
      py.setAdd(seen_nodes, node_id);
      var enriched: any = py.pyDict(node);
      py.setItem(enriched, "runtime_type", runtime_type);
      py.listAppend(nodes, enriched);
      if ((py.len(nodes) >= MAX_GRAPH_NODES)) {
        break;
      }
    }
    var edge: any;
    for (edge of py.iter(runtime_edges)) {
      var src: any = py.strip(py.toStr(py.get(edge, "from", "")));
      var dst: any = py.strip(py.toStr(py.get(edge, "to", "")));
      var relation: any = py.strip(py.toStr(py.get(edge, "relation", "related_to")));
      if ((!py.truthy(src) || !py.truthy(dst))) {
        continue;
      }
      var edge_key: any = [src, dst, relation];
      if (py.contains(seen_edges, edge_key)) {
        continue;
      }
      py.setAdd(seen_edges, edge_key);
      enriched = py.pyDict(edge);
      py.setItem(enriched, "runtime_type", runtime_type);
      py.listAppend(edges, enriched);
      if ((py.len(edges) >= MAX_GRAPH_EDGES)) {
        break;
      }
    }
  }
  return {"ir": "unified_runtime_graph", "nodes": py.sorted(nodes, {key: ((x: any) => py.toStr(py.get(x, "id", ""))) as (item: any) => any}), "edges": py.sorted(edges, {key: ((x: any) => [py.toStr(py.get(x, "from", "")), py.toStr(py.get(x, "to", "")), py.toStr(py.get(x, "relation", ""))]) as (item: any) => any}), "bounded": true};
}
