/**
 * Converted from Python: core/knowledge/ontology_validation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { checkOntologyConsistency } from "./ontologyConsistencyEngine.js";

export function validateOntologyEdge(edge: any): any {
  var ev: any = py.or2(py.get(edge, "evidence", []), () => ([]));
  if ((typeof ev === "string")) {
    ev = [ev];
  }
  var valid: any = py.and2(py.truthy(py.get(edge, "from")), () => (py.and2(py.truthy(py.get(edge, "to")), () => (py.and2(py.truthy(ev), () => (!py.contains(edge, "type")))))));
  return {...(edge), "valid": valid, "grounding": py.get(edge, "grounding", {"method": (py.truthy(ev) ? "evidence_required" : "invalid")}), "validation": checkOntologyConsistency([edge])};
}
export { checkOntologyConsistency };
