/**
 * Converted from Python: core/graph/semantic_partition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function partitionGraph(graph: any): any {
  var nodes: any = py.or2(py.get(graph, "nodes", []), () => ([]));
  var edges: any = py.or2(py.get(graph, "edges", []), () => ([]));
  var parent: Record<string, any> = {};
  function find(x: any): any {
    py.setdefault(parent, x, x);
    if (!py.eq(py.at(parent, x), x)) {
      py.setItem(parent, x, find(py.at(parent, x)));
    }
    return py.at(parent, x);
  }
  function union(a: any, b: any): any {
    const _d1 = py.iter([find(a), find(b)]) as any[];
    var ra: any = _d1[0];
    var rb: any = _d1[1];
    if (!py.eq(ra, rb)) {
      py.setItem(parent, rb, ra);
    }
  }
  var n: any;
  for (n of py.iter(nodes)) {
    if ((((n !== null && typeof n === "object" && !Array.isArray(n) && !(n instanceof Set) && !(n instanceof Map))) && py.truthy(py.get(n, "id")))) {
      find(py.toStr(py.at(n, "id")));
    }
  }
  var e: any;
  for (e of py.iter(edges)) {
    if ((((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map))) && py.truthy(py.get(e, "from")) && py.truthy(py.get(e, "to")))) {
      union(py.toStr(py.at(e, "from")), py.toStr(py.at(e, "to")));
    }
  }
  var components: Record<string, any> = {};
  var x: any;
  for (x of py.iter(parent)) {
    var root: any = find(x);
    py.listAppend(py.setdefault(components, root, []), x);
  }
  return {"partitions": [...py.iter(py.values(components))], "count": py.len(components)};
}
