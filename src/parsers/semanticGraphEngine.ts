/**
 * Converted from Python: core/parsers/semantic_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_GRAPH_NODES: any = 5000;
export let MAX_GRAPH_EDGES: any = 20000;
export function buildSemanticGraph(parsed: any): any {
  var symbols: any = py.or2(py.get(parsed, "symbols", {}), () => ({}));
  var imports: any = py.or2(py.get(parsed, "imports", {}), () => ({}));
  var calls: any = py.or2(py.get(parsed, "calls", {}), () => ({}));
  var source_id: any = py.toStr(py.or2(py.get(parsed, "source_id"), () => (py.or2(py.get(parsed, "language"), () => ("module")))));
  var node_ids: any = new Set([source_id]);
  var key: any;
  for (key of py.iter(["classes", "functions", "interfaces", "symbols"])) {
    var name: any;
    for (name of py.iter(py.or2(py.get(symbols, key, []), () => ([])))) {
      py.setAdd(node_ids, py.toStr(name));
    }
  }
  var edge: any;
  for (edge of py.iter(py.or2(py.get(imports, "edges", []), () => ([])))) {
    if (((edge !== null && typeof edge === "object" && !Array.isArray(edge) && !(edge instanceof Set) && !(edge instanceof Map)))) {
      py.setAdd(node_ids, py.toStr(py.get(edge, "to", "")));
    }
  }
  var edge_meta: Record<string, any> = {};
  for (edge of py.iter(py.or2(py.get(imports, "edges", []), () => ([])))) {
    if ((((edge !== null && typeof edge === "object" && !Array.isArray(edge) && !(edge instanceof Set) && !(edge instanceof Map))) && py.truthy(py.get(edge, "from")) && py.truthy(py.get(edge, "to")))) {
      key = [py.toStr(py.at(edge, "from")), py.toStr(py.at(edge, "to"))];
      py.setItem(edge_meta, key, "observed");
    }
  }
  for (edge of py.iter(py.or2(py.get(calls, "calls", []), () => ([])))) {
    if ((((edge !== null && typeof edge === "object" && !Array.isArray(edge) && !(edge instanceof Set) && !(edge instanceof Map))) && py.truthy(py.get(edge, "from")) && py.truthy(py.get(edge, "to")))) {
      const _d1 = py.iter([py.toStr(py.at(edge, "from")), py.toStr(py.at(edge, "to"))]) as any[];
      var f: any = _d1[0];
      var t: any = _d1[1];
      py.setAdd(node_ids, f);
      py.setAdd(node_ids, t);
      key = [f, t];
      py.setItem(edge_meta, key, (py.contains(edge_meta, key) ? py.get(edge_meta, key, "inferred") : "observed"));
    }
  }
  var nodes: any = py.iter(py.slice(py.sorted(py.iter(node_ids).filter((n: any) => py.truthy(n)).map((n: any) => n)), null, MAX_GRAPH_NODES)).map((nid: any) => ({"id": nid, "kind": "symbol", "metadata": {}}));
  var allowed: any = py.toSet(py.iter(nodes).map((n: any) => py.at(n, "id")));
  var edge_list: any = py.slice(py.iter(py.sorted(py.keys(edge_meta))).filter(([f, t]: any) => (py.contains(allowed, f) && py.contains(allowed, t))).map(([f, t]: any) => ({"from": f, "to": t, "metadata": {"edge_basis": py.get(edge_meta, [f, t], "observed"), "evidence": ["parser:graph"]}})), null, MAX_GRAPH_EDGES);
  return {"nodes": nodes, "edges": edge_list, "max_edges": MAX_GRAPH_EDGES};
}
