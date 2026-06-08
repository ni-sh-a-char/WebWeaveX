/**
 * Converted from Python: core/repository/reconstruction/runtime_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function buildRuntimeGraph(runtimes: any, services: any): any {
  var rs: any = py.sorted(py.toSet(py.or2(runtimes, () => ([]))));
  var sv: any = py.sorted(py.toSet(py.or2(services, () => ([]))));
  var edges: any = py.iter(sv).flatMap((s: any) => py.iter(rs).map((r: any) => ({"from": s, "to": r})));
  return {"nodes": py.sorted(py.toSet(py.add(rs, sv))), "edges": py.sorted(edges, {key: ((e: any) => [py.at(e, "from"), py.at(e, "to")]) as (item: any) => any})};
}
