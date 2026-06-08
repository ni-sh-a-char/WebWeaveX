/**
 * Converted from Python: core/evidence/semantic_fragility_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelFragility(evidence: any, ambiguities: any, contradiction_count: any = 0, parser_density: any = 0): any {
  var missing: any[] = [];
  if ((py.len(evidence) < 2)) {
    py.listAppend(missing, "low_evidence_density");
  }
  if (py.eq(parser_density, 0)) {
    py.listAppend(missing, "no_parser_grounding");
  }
  var pressure: any = (py.truthy(contradiction_count) ? [`contradiction:${py.toStr(contradiction_count)}`] : []);
  if (((py.len(evidence) >= 3) && !py.truthy(ambiguities) && py.eq(contradiction_count, 0))) {
    var level: any = "low";
    var cap: any = py.F(0.85);
  } else if ((py.len(evidence) >= 1)) {
    level = "medium";
    cap = py.F(0.55);
  } else {
    level = "high";
    cap = py.F(0.35);
  }
  if (py.truthy(ambiguities)) {
    level = (py.eq(level, "medium") ? "high" : level);
    cap = py.round(py.min([cap, py.F(0.45)]), 3);
  }
  return {"level": level, "basis": {"evidence_count": py.len(evidence), "ambiguity_count": py.len(ambiguities), "parser_density": parser_density}, "missing_support": py.sorted(py.toSet(missing)), "contradiction_pressure": pressure, "confidence_limits": {"max_score": cap}};
}
