/**
 * Converted from Python: core/distributed/semantic_service_mesh_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildSemanticServiceMesh(services: any): any {
  var nodes: any = py.sorted(services, {key: ((x: any) => py.toStr(py.get(x, "id"))) as (item: any) => any});
  var links: any[] = [];
  var idx: any;
  for (idx = 0; idx < py.sub(py.len(nodes), 1); idx++) {
    py.listAppend(links, {"from": py.at(py.at(nodes, idx), "id"), "to": py.at(py.at(nodes, py.add(idx, 1)), "id")});
  }
  return {"nodes": nodes, "links": links};
}
