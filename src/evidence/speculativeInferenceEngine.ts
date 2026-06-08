/**
 * Converted from Python: core/evidence/speculative_inference_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function _suppressionRecord(reason: any, evidence_gap: any, fragility_pressure: any = py.F(0.0), contradiction_pressure: any = py.F(0.0), ambiguity_pressure: any = py.F(0.0), confidence_caps: any = null): any {
  return {"reason": reason, "evidence_gap": evidence_gap, "fragility_pressure": {"level": fragility_pressure}, "contradiction_pressure": {"level": contradiction_pressure}, "ambiguity_pressure": {"level": ambiguity_pressure}, "confidence_caps": py.or2(confidence_caps, () => ({}))};
}
export function suppressSpeculativeInference(label: any, evidence: any, inferred: any = false, min_evidence: any = 2, fragility_level: any = "medium"): any {
  var gap: any = {"required": min_evidence, "actual": py.len(evidence), "inferred": inferred};
  var speculative: any = py.and2(inferred, () => ((py.len(evidence) < min_evidence)));
  var frag_map: any = {"high": py.F(0.8), "medium": py.F(0.5), "low": py.F(0.2)};
  if (py.truthy(speculative)) {
    return {"suppressed": true, "label": label, "record": _suppressionRecord(`speculative_${py.toStr(label)}`, gap, py.get(frag_map, fragility_level, py.F(0.5)))};
  }
  return {"suppressed": false, "label": label, "record": null};
}
export function collectSuppressedSpeculation(evidence: any, inferred: any, reconciled: any): any {
  var out: any[] = [];
  var key: any;
  for (key of py.iter(inferred)) {
    var r: any = suppressSpeculativeInference(`infer:${py.toStr(key)}`, evidence, true);
    if ((py.truthy(py.at(r, "suppressed")) && py.truthy(py.at(r, "record")))) {
      py.listAppend(out, py.at(r, "record"));
    }
  }
  if ((py.truthy(reconciled) && (py.len(evidence) < 2))) {
    r = suppressSpeculativeInference("reconcile", evidence);
    if ((py.truthy(py.at(r, "suppressed")) && py.truthy(py.at(r, "record")))) {
      py.listAppend(out, py.at(r, "record"));
    }
  }
  return out;
}
