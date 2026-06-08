/**
 * Converted from Python: core/evidence/provenance_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildProvenance(evidence: any, sources: any = null, grounding: any = null, lineage: any = null, confidence_basis: any = null): any {
  var ev: any = py.sorted(py.toSet(py.iter(py.or2(evidence, () => ([]))).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e))));
  var src: any = py.sorted(py.toSet(py.iter(py.or2(sources, () => (py.or2(evidence, () => ([]))))).filter((s: any) => py.truthy(s)).map((s: any) => py.toStr(s))));
  return {"evidence": ev, "sources": src, "grounding": (((grounding !== null && typeof grounding === "object" && !Array.isArray(grounding) && !(grounding instanceof Set) && !(grounding instanceof Map))) ? grounding : {}), "lineage": (((lineage !== null && typeof lineage === "object" && !Array.isArray(lineage) && !(lineage instanceof Set) && !(lineage instanceof Map))) ? lineage : {}), "confidence_basis": (((confidence_basis !== null && typeof confidence_basis === "object" && !Array.isArray(confidence_basis) && !(confidence_basis instanceof Set) && !(confidence_basis instanceof Map))) ? confidence_basis : {})};
}
