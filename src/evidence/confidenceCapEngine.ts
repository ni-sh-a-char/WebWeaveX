/**
 * Converted from Python: core/evidence/confidence_cap_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function applyConfidenceCaps(score: any, fragility: any, contradiction_count: any = 0, ambiguity_count: any = 0, unsupported_expansion_count: any = 0): any {
  var cap: any = py.toFloat(py.get(py.get(fragility, "confidence_limits", {}), "max_score", py.F(0.85)));
  var frag_penalty: any = py.get({"high": py.F(0.25), "medium": py.F(0.12), "low": py.F(0.0)}, py.get(fragility, "level", "medium"), py.F(0.12));
  var contradict_penalty: any = py.round(py.min([py.F(0.35), py.mul(contradiction_count, py.F(0.12))]), 3);
  var ambig_penalty: any = py.round(py.min([py.F(0.25), py.mul(ambiguity_count, py.F(0.08))]), 3);
  var expand_penalty: any = py.round(py.min([py.F(0.2), py.mul(unsupported_expansion_count, py.F(0.1))]), 3);
  var final: any = py.round(py.max([py.F(0.0), py.sub(py.sub(py.sub(py.sub(py.min([score, cap]), frag_penalty), contradict_penalty), ambig_penalty), expand_penalty)]), 3);
  return {"score": final, "caps": {"fragility_max": cap}, "fragility_penalties": {"amount": frag_penalty, "level": py.get(fragility, "level")}, "contradiction_penalties": {"amount": contradict_penalty, "count": contradiction_count}, "ambiguity_penalties": {"amount": ambig_penalty, "count": ambiguity_count}, "unsupported_expansion_penalties": {"amount": expand_penalty, "count": unsupported_expansion_count}, "deterministic_inputs": [`cap=${py.floatStr(cap)}`, `contradict=${py.toStr(contradiction_count)}`, `ambig=${py.toStr(ambiguity_count)}`, `expand=${py.toStr(unsupported_expansion_count)}`]};
}
