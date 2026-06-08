/**
 * Converted from Python: core/semantic/contradiction_pressure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeContradictionPressure(contradicted: any): any {
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.get(contradicted, "pairs", []) : []);
  var preserved: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.get(contradicted, "preserved", false) : false);
  var count: any = py.len(pairs);
  var pressure: any = py.round(py.min([py.F(1.0), py.mul(count, py.F(0.25))]), 3);
  return {"pressure": pressure, "pair_count": count, "preserved": preserved, "suppress_propagation": (count > 0), "suppress_reconciliation": (count > 0), "suppress_ontology_expansion": (count > 0), "suppress_topology_expansion": (count > 0), "confidence_reduction": py.round(py.min([py.F(0.4), py.mul(count, py.F(0.15))]), 3)};
}
