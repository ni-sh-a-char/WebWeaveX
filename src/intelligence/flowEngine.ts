/**
 * Converted from Python: core/intelligence/flow_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectFlows(edges: any): any {
  var flows: any[] = [];
  var edge: any;
  for (edge of py.iter(edges)) {
    py.listAppend(flows, {"from": py.get(edge, "from", ""), "to": py.get(edge, "to", "")});
  }
  return py.sorted(flows, {key: ((x: any) => [py.at(x, "from"), py.at(x, "to")]) as (item: any) => any});
}
