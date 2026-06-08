/**
 * Converted from Python: core/documents/causality_fragility_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelFragility } from "../evidence/semanticFragilityEngine.js";

export function assessCausalityFragility(edges: any): any {
  var evidence: any[] = [];
  var e: any;
  for (e of py.iter(py.or2(edges, () => ([])))) {
    py.extend(evidence, (((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map))) ? py.get(e, "evidence", []) : []));
  }
  return modelFragility(py.sorted(py.toSet(evidence)), [], 0, 0);
}
export { modelFragility };
