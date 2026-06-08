/**
 * Converted from Python: core/evidence/evidence_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildEvidenceGraph(claims: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var seen: Set<any> = new Set();
  var claim: any;
  for (claim of py.iter(py.or2(claims, () => ([])))) {
    if (!((claim !== null && typeof claim === "object" && !Array.isArray(claim) && !(claim instanceof Set) && !(claim instanceof Map)))) {
      continue;
    }
    var cid: any = py.toStr(py.get(claim, "id", ""));
    if ((!py.truthy(cid) || py.contains(seen, cid))) {
      continue;
    }
    py.setAdd(seen, cid);
    py.listAppend(nodes, {"id": cid, "kind": "claim", "metadata": {"sources": py.get(claim, "sources", [])}});
    var src: any;
    for (src of py.iter(py.or2(py.get(claim, "sources", []), () => ([])))) {
      var sid: any = `source:${py.toStr(src)}`;
      if (!py.contains(seen, sid)) {
        py.setAdd(seen, sid);
        py.listAppend(nodes, {"id": sid, "kind": "source", "metadata": {}});
      }
      py.listAppend(edges, {"from": sid, "to": cid});
    }
  }
  nodes = py.slice(nodes, null, 5000);
  var allowed: any = py.toSet(py.iter(nodes).map((n: any) => py.at(n, "id")));
  edges = py.slice(py.iter(py.sorted(edges, {key: ((x: any) => [py.at(x, "from"), py.at(x, "to")]) as (item: any) => any})).filter((e: any) => (py.contains(allowed, py.at(e, "from")) && py.contains(allowed, py.at(e, "to")))).map((e: any) => e), null, 20000);
  return {"nodes": nodes, "edges": edges};
}
