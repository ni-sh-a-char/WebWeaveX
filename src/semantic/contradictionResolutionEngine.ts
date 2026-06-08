/**
 * Converted from Python: core/semantic/contradiction_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconcileEvidence } from "../evidence/reconciliationEvidenceEngine.js";
import { preserveContradictions } from "./contradictionPreservationEngine.js";

export function resolveContradictionsWithoutCollapse(snippets: any): any {
  var preserved: any = preserveContradictions(snippets);
  var reconciliation: any = reconcileEvidence(py.range(py.len(py.or2(snippets, () => ([])))).map((i: any) => ({"key": "conflict", "value": py.toStr(i), "source": `snippet:${py.toStr(i)}`})));
  return {...(preserved), "resolution": reconciliation, "collapsed": false, "preserved_interpretations": py.get(preserved, "conflicting_claims", [])};
}
export { preserveContradictions, reconcileEvidence };
