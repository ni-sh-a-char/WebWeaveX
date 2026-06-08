/**
 * Converted from Python: core/graph/semantic_cycle_analysis_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectCycles(graph: any, max_depth: any = 50): any {
  var edges: any = py.or2(py.get(graph, "edges", []), () => ([]));
  var adj: Record<string, any> = {};
  var e: any;
  for (e of py.iter(edges)) {
    if ((((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map))) && py.truthy(py.get(e, "from")) && py.truthy(py.get(e, "to")))) {
      py.listAppend(py.setdefault(adj, py.toStr(py.at(e, "from")), []), py.toStr(py.at(e, "to")));
    }
  }
  var cycles: any[] = [];
  var visited: Set<any> = new Set();
  var stack: Set<any> = new Set();
  var path: any[] = [];
  function dfs(n: any, depth: any): any {
    if (py.gt(depth, max_depth)) {
      return;
    }
    if (py.contains(stack, n)) {
      if (py.contains(path, n)) {
        var i: any = py.index(path, n);
        py.listAppend(cycles, py.add(py.slice(path, i, null), [n]));
      }
      return;
    }
    if (py.contains(visited, n)) {
      return;
    }
    py.setAdd(visited, n);
    py.setAdd(stack, n);
    py.listAppend(path, n);
    var nb: any;
    for (nb of py.iter(py.get(adj, n, []))) {
      dfs(nb, py.add(depth, 1));
    }
    py.pop(path);
    py.remove(stack, n);
  }
  var start: any;
  for (start of py.iter(py.slice([...py.iter(py.keys(adj))], null, 100))) {
    dfs(start, 0);
  }
  return {"cycles": py.slice(cycles, null, 20), "cycle_count": py.len(cycles), "bounded": max_depth, "contradiction_pressure": py.min([py.F(1.0), py.mul(py.len(cycles), py.F(0.2))])};
}
