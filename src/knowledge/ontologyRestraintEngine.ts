/**
 * Converted from Python: core/knowledge/ontology_restraint_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { suppressSpeculativeOntologyEdge } from "./speculativeOntologyEngine.js";

export function restrainOntologyEdge(edge: any): any {
  var humbled: any = suppressSpeculativeOntologyEdge(edge);
  return {...(humbled), "restraint": {"expansion_allowed": !py.truthy(py.get(py.get(humbled, "unsupported", {}), "edge", true))}, "lineage": py.get(edge, "lineage", {})};
}
export { suppressSpeculativeOntologyEdge };
