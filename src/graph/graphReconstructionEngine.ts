/**
 * Converted from Python: core/graph/graph_reconstruction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_NODES: any = 5000;
export let MAX_EDGES: any = 20000;
export function _nodeId(value: any): any {
  return py.strip(py.toStr(py.or2(value, () => (""))));
}
export function normalizeGraphNodes(graph: any): any {
  var nodes: any[] = [];
  var raw: any;
  for (raw of py.iter(py.or2(py.get(graph, "nodes", []), () => ([])))) {
    if ((typeof raw === "string")) {
      py.listAppend(nodes, {"id": _nodeId(raw), "kind": "structural", "metadata": {}});
      continue;
    }
    if (!((raw !== null && typeof raw === "object" && !Array.isArray(raw) && !(raw instanceof Set) && !(raw instanceof Map)))) {
      continue;
    }
    var nid: any = _nodeId(py.get(raw, "id"));
    if (!py.truthy(nid)) {
      continue;
    }
    var kind: any = py.or2(py.get(raw, "kind"), () => ("structural"));
    var metadata: any = (((py.get(raw, "metadata") !== null && typeof py.get(raw, "metadata") === "object" && !Array.isArray(py.get(raw, "metadata")) && !(py.get(raw, "metadata") instanceof Set) && !(py.get(raw, "metadata") instanceof Map))) ? py.get(raw, "metadata") : {});
    py.listAppend(nodes, {"id": nid, "kind": py.toStr(kind), "metadata": metadata});
  }
  return {...(graph), "nodes": nodes};
}
export function reconstructGraph(system_graph: any, max_edges: any = MAX_EDGES, max_nodes: any = MAX_NODES): any {
  if (!((system_graph !== null && typeof system_graph === "object" && !Array.isArray(system_graph) && !(system_graph instanceof Set) && !(system_graph instanceof Map)))) {
    return {"nodes": [], "edges": [], "max_edges": max_edges};
  }
  var raw_nodes: any = py.or2(py.get(system_graph, "nodes", []), () => ([]));
  var raw_edges: any = py.or2(py.get(system_graph, "edges", []), () => ([]));
  var components: any = py.or2(py.get(system_graph, "components", []), () => ([]));
  var relationships: any = py.or2(py.get(system_graph, "relationships", []), () => ([]));
  var node_set: Set<any> = new Set();
  var n: any;
  for (n of py.iter(raw_nodes)) {
    if (((n !== null && typeof n === "object" && !Array.isArray(n) && !(n instanceof Set) && !(n instanceof Map)))) {
      py.setAdd(node_set, _nodeId(py.get(n, "id")));
    } else {
      py.setAdd(node_set, _nodeId(n));
    }
  }
  var c: any;
  for (c of py.iter(components)) {
    if (((c !== null && typeof c === "object" && !Array.isArray(c) && !(c instanceof Set) && !(c instanceof Map)))) {
      py.setAdd(node_set, _nodeId(py.get(c, "name")));
    }
  }
  var edge_set: Set<any> = new Set();
  var merged_edges: any[] = [];
  py.extend(merged_edges, ((Array.isArray(raw_edges)) ? raw_edges : []));
  py.extend(merged_edges, ((Array.isArray(relationships)) ? relationships : []));
  var e: any;
  for (e of py.iter(merged_edges)) {
    if (!((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))) {
      continue;
    }
    if (py.contains(e, "type")) {
      continue;
    }
    var f: any = _nodeId(py.get(e, "from"));
    var t: any = _nodeId(py.get(e, "to"));
    if ((!py.truthy(f) || !py.truthy(t))) {
      continue;
    }
    py.setAdd(node_set, f);
    py.setAdd(node_set, t);
    py.setAdd(edge_set, [f, t]);
  }
  var nodes: any = py.iter(py.slice(py.sorted(py.iter(node_set).filter((n: any) => py.truthy(n)).map((n: any) => n)), null, max_nodes)).map((nid: any) => ({"id": nid, "kind": "structural", "metadata": {}}));
  var allowed: any = py.toSet(py.iter(nodes).map((n: any) => py.at(n, "id")));
  var edges: any = py.slice(py.iter(py.sorted(edge_set)).filter(([f, t]: any) => (py.contains(allowed, f) && py.contains(allowed, t))).map(([f, t]: any) => ({"from": f, "to": t})), null, max_edges);
  return {"nodes": nodes, "edges": edges, "max_edges": max_edges};
}
export function buildSemanticGraphFromIds(node_ids: any, edges: any, max_nodes: any = MAX_NODES, max_edges: any = MAX_EDGES): any {
  var raw_nodes: any = py.iter(node_ids).filter((n: any) => py.truthy(n)).map((n: any) => ({"id": py.toStr(n), "kind": "structural", "metadata": {}}));
  return reconstructGraph({"nodes": raw_nodes, "edges": edges}, max_edges, max_nodes);
}
export function boundGraphMemory(graph: any, max_nodes: any = MAX_NODES, max_edges: any = MAX_EDGES): any {
  return reconstructGraph(graph, max_edges, max_nodes);
}
export function scoreGraph(graph: any): any {
  var nodes: any = (((graph !== null && typeof graph === "object" && !Array.isArray(graph) && !(graph instanceof Set) && !(graph instanceof Map))) ? py.get(graph, "nodes", []) : []);
  var edges: any = (((graph !== null && typeof graph === "object" && !Array.isArray(graph) && !(graph instanceof Set) && !(graph instanceof Map))) ? py.get(graph, "edges", []) : []);
  return {"node_count": py.len(nodes), "edge_count": py.len(edges), "density": py.round(py.div(py.len(edges), py.max([1, py.len(nodes)])), 4)};
}
