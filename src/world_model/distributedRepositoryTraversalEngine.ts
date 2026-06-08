/**
 * Converted from Python: core/world_model/distributed_repository_traversal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_VISITS: any = 100000;
export function traverseRepositoryWorld(graph: any, start: any): any {
  var queue: any = py.deque([start]);
  var visited: any[] = [];
  var seen: Set<any> = new Set();
  while ((py.truthy(queue) && (py.len(visited) < MAX_VISITS))) {
    var node: any = py.popleft(queue);
    if (py.contains(seen, node)) {
      continue;
    }
    py.setAdd(seen, node);
    py.listAppend(visited, node);
    var neighbors: any = py.sorted(py.iter(py.get(graph, "edges", [])).filter((edge: any) => (py.eq(py.get(edge, "from"), node) && py.truthy(py.get(edge, "to")))).map((edge: any) => py.toStr(py.get(edge, "to"))));
    var nxt: any;
    for (nxt of py.iter(neighbors)) {
      if (!py.contains(seen, nxt)) {
        py.listAppend(queue, nxt);
      }
    }
  }
  return {"visited": visited, "count": py.len(visited), "bounded": (py.len(visited) < MAX_VISITS)};
}
