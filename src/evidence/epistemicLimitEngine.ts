/**
 * Converted from Python: core/evidence/epistemic_limit_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelEpistemicLimits(evidence: any, parser_density: any, fragility: any): any {
  var cannot_conclude: any[] = [];
  if ((py.len(evidence) < 2)) {
    py.listAppend(cannot_conclude, "definitive_semantic_conclusion");
  }
  if (py.eq(parser_density, 0)) {
    py.listAppend(cannot_conclude, "parser_grounded_conclusion");
  }
  if (py.eq(py.get(fragility, "level"), "high")) {
    py.listAppend(cannot_conclude, "high_confidence_claim");
  }
  return {"cannot_conclude": py.sorted(py.toSet(cannot_conclude)), "exceeds_evidence": (py.len(evidence) < 1), "exceeds_parser_grounding": py.eq(parser_density, 0), "exceeds_corroboration": (py.len(evidence) < 2), "max_confidence": py.get(py.get(fragility, "confidence_limits", {}), "max_score", py.F(0.5))};
}
