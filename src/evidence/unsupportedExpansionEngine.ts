/**
 * Converted from Python: core/evidence/unsupported_expansion_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectUnsupportedExpansion(evidence: any, expansion_type: any, count: any): any {
  var suppressed: any = py.and2((count > 0), () => ((py.len(evidence) < 2)));
  return {"expansion_type": expansion_type, "count": count, "suppressed": suppressed, "unsupported_expansions": (py.truthy(suppressed) ? py.range(count).map((i: any) => `${py.toStr(expansion_type)}:${py.toStr(i)}`) : []), "reason": (py.truthy(suppressed) ? "insufficient_evidence" : "allowed")};
}
