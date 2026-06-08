/**
 * Converted from Python: core/graph/reasoning/graph_traversal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function graphTraverse(graph: any, start: any, max_steps: any = 1000): any {
  var adj: Record<string, any> = {};
  var e: any;
  for (e of py.iter(py.get(py.or2(graph, () => ({})), "edges", []))) {
    if (!((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))) {
      continue;
    }
    const _d1 = py.iter([py.get(e, "from", ""), py.get(e, "to", "")]) as any[];
    var f: any = _d1[0];
    var t: any = _d1[1];
    if ((py.truthy(f) && py.truthy(t))) {
      py.listAppend(py.setdefault(adj, f, []), t);
    }
  }
  var k: any;
  for (k of py.iter(adj)) {
    py.setItem(adj, k, py.sorted(py.toSet(py.at(adj, k))));
  }
  var order: any[] = [];
  var q: any = [start];
  var seen: any = py.toSet([start]);
  while ((py.truthy(q) && (py.len(order) < max_steps))) {
    var cur: any = py.pop(q, 0);
    py.listAppend(order, cur);
    var nxt: any;
    for (nxt of py.iter(py.get(adj, cur, []))) {
      if (py.contains(seen, nxt)) {
        continue;
      }
      py.setAdd(seen, nxt);
      py.listAppend(q, nxt);
    }
  }
  return {"order": order};
}
