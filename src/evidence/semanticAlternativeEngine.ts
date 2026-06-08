/**
 * Converted from Python: core/evidence/semantic_alternative_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelSemanticAlternatives(observed: any, inferred: any): any {
  var alts: any = py.iter(py.sorted(py.bitor(py.toSet(observed), py.toSet(inferred)))).map((k: any) => ({"key": k, "source": (py.contains(observed, k) ? "observed" : "inferred")}));
  return {"alternatives": py.slice(alts, null, 15), "preserved": py.or2((py.len(alts) > 1), () => (!py.truthy(alts)))};
}
