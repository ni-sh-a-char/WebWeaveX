/**
 * Converted from Python: core/intelligence/cluster_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectClusters(nodes: any, edges: any): any {
  var adj: Record<string, any> = {};
  var node: any;
  for (node of py.iter(nodes)) {
    py.setItem(adj, py.at(node, "id"), new Set());
  }
  var edge: any;
  for (edge of py.iter(edges)) {
    var f: any = py.get(edge, "from", "");
    var t: any = py.get(edge, "to", "");
    if (!py.contains(adj, f)) {
      py.setItem(adj, f, new Set());
    }
    if (!py.contains(adj, t)) {
      py.setItem(adj, t, new Set());
    }
    py.setAdd(py.at(adj, f), t);
    py.setAdd(py.at(adj, t), f);
  }
  var visited: Set<any> = new Set();
  var clusters: any[] = [];
  for (node of py.iter(adj)) {
    if (!py.contains(visited, node)) {
      var stack: any = [node];
      var cluster: any[] = [];
      while (py.truthy(stack)) {
        var n: any = py.pop(stack);
        if (!py.contains(visited, n)) {
          py.setAdd(visited, n);
          py.listAppend(cluster, n);
          var neighbor: any;
          for (neighbor of py.iter(py.get(adj, n, new Set()))) {
            if (!py.contains(visited, neighbor)) {
              py.listAppend(stack, neighbor);
            }
          }
        }
      }
      if (py.truthy(cluster)) {
        py.listAppend(clusters, py.sorted(cluster));
      }
    }
  }
  return py.sorted(clusters);
}
