/**
 * Converted from Python: core/knowledge/ontology_fragility_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelFragility } from "../evidence/semanticFragilityEngine.js";

export function assessOntologyEdgeFragility(edge: any): any {
  var ev: any = py.or2(py.get(edge, "evidence", []), () => ([]));
  var amb: any = py.or2(py.get(edge, "ambiguities", []), () => ([]));
  return modelFragility(ev, amb, 0, 0);
}
export { modelFragility };
