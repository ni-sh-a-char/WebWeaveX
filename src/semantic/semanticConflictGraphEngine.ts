/**
 * Converted from Python: core/semantic/semantic_conflict_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildConflictGraph(conflicts: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var seen: Set<any> = new Set();
  var c: any;
  for (c of py.iter(py.or2(conflicts, () => ([])))) {
    if (!((c !== null && typeof c === "object" && !Array.isArray(c) && !(c instanceof Set) && !(c instanceof Map)))) {
      continue;
    }
    const _d1 = py.iter([py.toStr(py.get(c, "from", "")), py.toStr(py.get(c, "to", ""))]) as any[];
    var a: any = _d1[0];
    var b: any = _d1[1];
    if ((!py.truthy(a) || !py.truthy(b))) {
      continue;
    }
    var nid: any;
    for (nid of py.iter([a, b])) {
      if (!py.contains(seen, nid)) {
        py.setAdd(seen, nid);
        py.listAppend(nodes, {"id": nid, "kind": "claim", "metadata": {"conflict": true}});
      }
    }
    py.listAppend(edges, {"from": a, "to": b, "metadata": {"edge_basis": "contradicted", "evidence": py.get(c, "evidence", [])}});
  }
  return {"nodes": py.sorted(nodes, {key: ((n: any) => py.at(n, "id")) as (item: any) => any}), "edges": edges};
}
