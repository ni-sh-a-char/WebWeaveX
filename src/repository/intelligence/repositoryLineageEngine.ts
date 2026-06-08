/**
 * Converted from Python: core/repository/intelligence/repository_lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function buildLineage(paths: any): any {
  paths = py.sorted(py.toSet(py.or2(paths, () => ([]))));
  var edges: any[] = [];
  var p: any;
  for (p of py.iter(paths)) {
    var parts: any = py.split(p, "/");
    var i: any;
    for (i = 1; i < py.len(parts); i++) {
      py.listAppend(edges, {"from": py.join("/", py.slice(parts, null, i)), "to": py.join("/", py.slice(parts, null, py.add(i, 1)))});
    }
  }
  edges = py.sorted(py.toSet(py.iter(edges).map((e: any) => [py.at(e, "from"), py.at(e, "to")])));
  return {"nodes": py.sorted(py.toSet(py.add(paths, py.iter(edges).flatMap((e: any) => py.iter(e).map((x: any) => x))))), "edges": py.iter(edges).map(([a, b]: any) => ({"from": a, "to": b}))};
}
