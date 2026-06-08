/**
 * Converted from Python: core/evidence/recursive_submission_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectRecursiveSubmission(reconciled_eq_inferred: any, depth: any, evidence_count: any): any {
  var submission: any = py.and2(reconciled_eq_inferred, () => (py.and2((depth >= 2), () => ((evidence_count < 2)))));
  return {"submission": submission, "suppress": submission};
}
