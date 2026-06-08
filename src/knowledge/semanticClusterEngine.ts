/**
 * Converted from Python: core/knowledge/semantic_cluster_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function clusterSemanticGraph(graph: any): any {
  var nodes: any = py.sorted(py.toSet(py.get(py.or2(graph, () => ({})), "nodes", [])));
  var clusters: Record<string, any> = {};
  var n: any;
  for (n of py.iter(nodes)) {
    var key: any = (py.contains(n, ".") ? py.at(py.split(n, "."), 0) : String(py.slice(n, null, 1)).toLowerCase());
    py.listAppend(py.setdefault(clusters, key, []), n);
  }
  return {"clusters": Object.fromEntries(py.iter(py.sorted(py.items(clusters))).map(([k, v]: any) => ([k, py.sorted(v)] as [any, any])))};
}
