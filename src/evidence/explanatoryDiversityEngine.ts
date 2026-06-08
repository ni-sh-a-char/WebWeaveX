/**
 * Converted from Python: core/evidence/explanatory_diversity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelExplanatoryDiversity(inferred: any, evidence: any): any {
  var alternatives: any = py.iter(py.slice([...py.iter(py.keys(inferred))], null, 8)).map((k: any) => ({"explanation": k, "grounded": py.contains(py.toStr(evidence), k)}));
  return {"preserved": true, "alternatives": alternatives, "collapse_suppressed": true, "narrative_monopoly": py.and2((py.len(alternatives) <= 1), () => ((py.len(evidence) < 2)))};
}
