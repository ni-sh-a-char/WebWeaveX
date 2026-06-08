/**
 * Converted from Python: core/query/graph_scale_traversal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_GRAPH_VISITS: any = 10000;
export function traverseLargeGraph(graph: any, start: any): any {
  var adjacency: Record<string, any> = {};
  var edge: any;
  for (edge of py.iter(py.get(graph, "edges", []))) {
    py.listAppend(py.setdefault(adjacency, py.at(edge, "from"), []), py.at(edge, "to"));
  }
  var queue: any = py.deque([start]);
  var visited: any[] = [];
  var seen: Set<any> = new Set();
  while ((py.truthy(queue) && (py.len(visited) < MAX_GRAPH_VISITS))) {
    var node: any = py.popleft(queue);
    if (py.contains(seen, node)) {
      continue;
    }
    py.setAdd(seen, node);
    py.listAppend(visited, node);
    var nxt: any;
    for (nxt of py.iter(py.sorted(py.get(adjacency, node, [])))) {
      py.listAppend(queue, nxt);
    }
  }
  return {"visited": visited, "count": py.len(visited), "bounded": true};
}
