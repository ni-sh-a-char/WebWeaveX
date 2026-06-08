/**
 * Converted from Python: core/repository/topology_fragility_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelFragility } from "../evidence/semanticFragilityEngine.js";

export function assessTopologyEdgeFragility(edge: any): any {
  var ev: any = py.or2(py.get(edge, "evidence", []), () => ([]));
  var amb: any = py.or2(py.get(edge, "ambiguities", []), () => ([]));
  var parser_density: any = (py.truthy(py.get(edge, "parser_basis")) ? 1 : 0);
  return modelFragility(ev, amb, 0, parser_density);
}
export { modelFragility };
