/**
 * Converted from Python: core/graph/topology_proof_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function proveTopology(graph: any): any {
  var edges: any = py.or2(py.get(graph, "edges", []), () => ([]));
  var degree: Record<string, any> = {};
  var e: any;
  for (e of py.iter(edges)) {
    if (!((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))) {
      continue;
    }
    const _d1 = py.iter([py.get(e, "from"), py.get(e, "to")]) as any[];
    var f: any = _d1[0];
    var t: any = _d1[1];
    if (py.truthy(f)) {
      py.setItem(degree, py.toStr(f), py.add(py.get(degree, py.toStr(f), 0), 1));
    }
    if (py.truthy(t)) {
      py.setItem(degree, py.toStr(t), py.add(py.get(degree, py.toStr(t), 0), 1));
    }
  }
  var hubs: any = py.sorted(py.items(degree).filter(([n, d]: any) => (d >= 3)).map(([n, d]: any) => n));
  var max_deg: any = (py.truthy(degree) ? py.max(py.values(degree)) : 0);
  return {"proved": true, "max_degree": max_deg, "hubs": py.slice(hubs, null, 20), "edge_count": py.len(edges), "deterministic_inputs": [`max_degree=${py.toStr(max_deg)}`, `hubs=${py.toStr(py.len(hubs))}`]};
}
