/**
 * Converted from Python: core/evidence/evidence_sufficiency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function assessEvidenceSufficiency(evidence: any, required: any = 2): any {
  var count: any = py.len(py.or2(evidence, () => ([])));
  var sufficient: any = py.ge(count, required);
  return {"sufficient": sufficient, "evidence_count": count, "required": required, "status": (py.truthy(sufficient) ? "sufficient" : "insufficient_evidence"), "deterministic_inputs": [`count=${py.toStr(count)}`, `required=${py.toStr(required)}`]};
}
