/**
 * Converted from Python: core/evidence/unsupported_inference_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function suppressUnsupportedInference(evidence: any, inferred: any, observed: any, min_evidence: any = 2): any {
  var unsupported_dims: any[] = [];
  var suppressed: any[] = [];
  if (((py.len(evidence) < min_evidence) && py.truthy(inferred))) {
    py.listAppend(unsupported_dims, "inferred_without_evidence");
    suppressed = py.sorted(py.keys(inferred));
  }
  if ((py.truthy(inferred) && !py.truthy(observed))) {
    py.listAppend(unsupported_dims, "inferred_without_observation");
  }
  return {"suppressed": py.truthy(suppressed), "unsupported_dimensions": py.sorted(py.toSet(unsupported_dims)), "suppressed_keys": suppressed, "allowed_inference": (py.len(evidence) >= min_evidence)};
}
