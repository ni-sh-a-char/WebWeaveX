/**
 * Converted from Python: core/determinism/runtime_graph_parity.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function normalizeRuntimeGraph(graph: any): any {
  var nodes: any = py.sorted([...py.iter(py.or2(py.get(graph, "nodes"), () => ([])))], {key: ((n: any) => `${py.toStr(py.get(n, "id", ""))}|${py.toStr(py.get(n, "type", ""))}|${py.toStr(py.get(n, "name", ""))}`) as (item: any) => any});
  var edges: any = py.sorted([...py.iter(py.or2(py.get(graph, "edges"), () => ([])))], {key: ((e: any) => `${py.toStr(py.or2(py.get(e, "source"), () => (py.get(e, "from", ""))))}|${py.toStr(py.or2(py.get(e, "target"), () => (py.get(e, "to", ""))))}|${py.toStr(py.get(e, "type", ""))}`) as (item: any) => any});
  return {"nodes": nodes, "edges": edges, "bounded": true};
}
export function buildParityRuntimeGraph(sources: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var idx: any = 0;
  var kind: any;
  var payload: any;
  for ([kind, payload] of py.iter(py.sorted(py.items(sources), {key: ((kv: any) => py.at(kv, 0)) as (item: any) => any}))) {
    py.listAppend(nodes, {"id": `node:${py.toStr(kind)}:${py.toStr(idx)}`, "type": kind, "payload": payload});
    idx = py.add(idx, 1);
  }
  if ((py.len(nodes) > 1)) {
    var i: any;
    for (i = 1; i < py.len(nodes); i++) {
      py.listAppend(edges, {"source": py.at(py.at(nodes, 0), "id"), "target": py.at(py.at(nodes, i), "id"), "type": "runtime_link"});
    }
  }
  return normalizeRuntimeGraph({"nodes": nodes, "edges": edges, "bounded": true});
}
