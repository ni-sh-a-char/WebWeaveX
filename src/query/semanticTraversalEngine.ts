/**
 * Converted from Python: core/query/semantic_traversal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_TRAVERSAL_DEPTH: any = 50;
export function traverseGraph(adjacency: any, start: any): any {
  var visited: Set<any> = new Set();
  var queue: any = py.deque([[start, 0]]);
  var ordered: any[] = [];
  while (py.truthy(queue)) {
    const _d1 = py.iter(py.popleft(queue)) as any[];
    var node: any = _d1[0];
    var depth: any = _d1[1];
    if (py.gt(depth, MAX_TRAVERSAL_DEPTH)) {
      continue;
    }
    if (py.contains(visited, node)) {
      continue;
    }
    py.setAdd(visited, node);
    py.listAppend(ordered, node);
    var nxt: any;
    for (nxt of py.iter(py.sorted(py.get(adjacency, node, [])))) {
      py.listAppend(queue, [nxt, py.add(depth, 1)]);
    }
  }
  return ordered;
}
export function semanticTraverse(graph: any, start: any, max_depth: any = 10): any {
  var edges: any = py.or2(py.get(graph, "edges", []), () => ([]));
  var adj: Record<string, any> = {};
  var e: any;
  for (e of py.iter(edges)) {
    if ((((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map))) && py.truthy(py.get(e, "from")) && py.truthy(py.get(e, "to")))) {
      py.listAppend(py.setdefault(adj, py.toStr(py.at(e, "from")), []), py.toStr(py.at(e, "to")));
    }
  }
  var visited: Set<any> = new Set();
  var order: any[] = [];
  function dfs(n: any, d: any): any {
    if ((py.gt(d, max_depth) || py.contains(visited, n))) {
      return;
    }
    py.setAdd(visited, n);
    py.listAppend(order, n);
    var nb: any;
    for (nb of py.iter(py.get(adj, n, []))) {
      dfs(nb, py.add(d, 1));
    }
  }
  if (py.truthy(start)) {
    dfs(start, 0);
  }
  return {"order": order, "visited_count": py.len(visited), "max_depth": max_depth, "bounded": true};
}
