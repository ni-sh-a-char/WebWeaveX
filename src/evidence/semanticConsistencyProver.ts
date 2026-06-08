/**
 * Converted from Python: core/evidence/semantic_consistency_prover.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { assessSemanticConsistency } from "./semanticConsistencyEngine.js";

export function proveConsistency(observed: any, inferred: any, reconciled: any): any {
  var r: any = assessSemanticConsistency(observed, inferred, reconciled);
  return {...(r), "proved": py.at(r, "consistent"), "proof": "key_overlap_consistency"};
}
export { assessSemanticConsistency };
