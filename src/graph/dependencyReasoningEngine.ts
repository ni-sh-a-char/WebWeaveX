/**
 * Converted from Python: core/graph/dependency_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function reasonDependencies(graph: any): any {
  var edges: any = (((graph !== null && typeof graph === "object" && !Array.isArray(graph) && !(graph instanceof Set) && !(graph instanceof Map))) ? py.get(graph, "edges", []) : []);
  var deps: Record<string, any> = {};
  var e: any;
  for (e of py.iter(edges)) {
    if (!((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))) {
      continue;
    }
    const _d1 = py.iter([py.toStr(py.get(e, "from", "")), py.toStr(py.get(e, "to", ""))]) as any[];
    var f: any = _d1[0];
    var t: any = _d1[1];
    if ((!py.truthy(f) || !py.truthy(t))) {
      continue;
    }
    py.setAdd(py.setdefault(deps, f, new Set()), t);
  }
  var chains: any = py.slice(py.sorted(py.items(deps).map(([f, ts]: any) => ({"from": f, "to": py.sorted(ts)})), {key: ((x: any) => py.at(x, "from")) as (item: any) => any}), null, 500);
  return {"dependency_chains": chains, "root_count": py.len(deps)};
}
