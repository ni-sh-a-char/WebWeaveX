/**
 * Converted from Python: core/native/electron/electron_route_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractElectronRoutes(routes: any = null): any {
  var route_list: any = py.sorted(py.or2(routes, () => ([{"path": "/", "order": 0}])), {key: ((r: any) => [py.toInt(py.get(r, "order", 0)), py.toStr(py.get(r, "path", ""))]) as (item: any) => any});
  var nodes: any = py.iter(route_list).map((r: any) => ({"id": `route:${py.toStr(py.at(r, "path"))}`, "type": "route", "path": py.at(r, "path")}));
  var edges: any[] = [];
  var i: any;
  for (i = 0; i < py.sub(py.len(route_list), 1); i++) {
    py.listAppend(edges, {"source": `route:${py.toStr(py.at(py.at(route_list, i), "path"))}`, "target": `route:${py.toStr(py.at(py.at(route_list, py.add(i, 1)), "path"))}`, "type": "navigate"});
  }
  return {"routes": route_list, "graph": {"nodes": nodes, "edges": edges, "bounded": true}, "bounded": true};
}
