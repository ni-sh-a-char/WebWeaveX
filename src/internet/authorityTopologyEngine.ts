/**
 * Converted from Python: core/internet/authority_topology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { scoreAuthority } from "./authorityEngine.js";

export function buildAuthorityTopology(urls: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var u: any;
  for (u of py.iter(py.or2(urls, () => ([])))) {
    var auth: any = scoreAuthority(u);
    py.listAppend(nodes, {"id": u, "authority": py.get(auth, "authority_score", 0)});
  }
  var i: any;
  for (i = 0; i < py.sub(py.len(nodes), 1); i++) {
    py.listAppend(edges, {"from": py.at(py.at(nodes, i), "id"), "to": py.at(py.at(nodes, py.add(i, 1)), "id"), "relation": "authority_chain"});
  }
  return {"nodes": nodes, "edges": edges};
}
export { scoreAuthority };
