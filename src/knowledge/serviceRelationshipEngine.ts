/**
 * Converted from Python: core/knowledge/service_relationship_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildServiceRelationships(services: any): any {
  var ordered: any = py.sorted(py.toSet(py.or2(services, () => ([]))));
  var edges: any = py.iter(ordered).map((s: any) => ({"from": "service", "to": s}));
  return {"nodes": py.add(["service"], ordered), "edges": edges};
}
