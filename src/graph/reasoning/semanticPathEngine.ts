/**
 * Converted from Python: core/graph/reasoning/semantic_path_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function _adj(graph: any): any {
  var a: Record<string, any> = {};
  var e: any;
  for (e of py.iter(py.get(py.or2(graph, () => ({})), "edges", []))) {
    if (!((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))) {
      continue;
    }
    const _d1 = py.iter([py.get(e, "from", ""), py.get(e, "to", "")]) as any[];
    var f: any = _d1[0];
    var t: any = _d1[1];
    if ((py.truthy(f) && py.truthy(t))) {
      py.listAppend(py.setdefault(a, f, []), t);
    }
  }
  var k: any;
  for (k of py.iter(a)) {
    py.setItem(a, k, py.sorted(py.toSet(py.at(a, k))));
  }
  return a;
}
export function semanticPaths(graph: any, start: any, depth: any = 3): any {
  var adj: any = _adj(graph);
  var paths: any[] = [];
  var q: any = [[start, [start], 0]];
  while (py.truthy(q)) {
    const _d2 = py.iter(py.pop(q, 0)) as any[];
    var cur: any = _d2[0];
    var path: any = _d2[1];
    var d: any = _d2[2];
    if (py.ge(d, depth)) {
      py.listAppend(paths, path);
      continue;
    }
    var nxts: any = py.get(adj, cur, []);
    if (!py.truthy(nxts)) {
      py.listAppend(paths, path);
    }
    var n: any;
    for (n of py.iter(nxts)) {
      if (py.contains(path, n)) {
        continue;
      }
      py.listAppend(q, [n, py.add(path, [n]), py.add(d, 1)]);
    }
  }
  return {"paths": py.sorted(paths)};
}
