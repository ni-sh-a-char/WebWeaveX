/**
 * Converted from Python: core/evidence/recursive_evidence_ancestry_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function trackRecursiveEvidenceAncestry(evidence: any, depth: any): any {
  var detached: any = py.and2((depth > 3), () => ((py.len(evidence) < 2)));
  return {"ancestry": [...py.iter(evidence)], "depth": depth, "detached": detached, "suppress_stabilization": detached};
}
