/**
 * Converted from Python: core/graph/semantic_edge_validation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function validateSemanticEdge(edge: any): any {
  if (py.contains(edge, "type")) {
    return {"valid": false, "reason": "forbidden_type_field"};
  }
  if ((!py.truthy(py.get(edge, "from")) || !py.truthy(py.get(edge, "to")))) {
    return {"valid": false, "reason": "missing_endpoints"};
  }
  var ev: any = py.or2(py.get(edge, "evidence", []), () => ([]));
  if ((typeof ev === "string")) {
    ev = [ev];
  }
  return {"valid": py.truthy(ev), "evidence_count": py.len(ev), "grounding": py.get(edge, "grounding", {}), "uncertainty": py.get(edge, "uncertainty", {}), "justification": py.get(edge, "justification", {})};
}
