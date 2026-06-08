/**
 * Converted from Python: core/evidence/narrative_hallucination_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectNarrativeHallucination(inferred: any, evidence: any, parser_grounded: any): any {
  var hallucinated: any = py.and2(py.truthy(inferred), () => (py.and2(!py.truthy(parser_grounded), () => ((py.len(evidence) < 1)))));
  return {"hallucination_risk": hallucinated, "suppressed": hallucinated, "reason": (py.truthy(hallucinated) ? "narrative_without_parser" : null)};
}
