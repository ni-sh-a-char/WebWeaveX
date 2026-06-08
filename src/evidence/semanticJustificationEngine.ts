/**
 * Converted from Python: core/evidence/semantic_justification_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildJustification(evidence: any, lineage: any, uncertainty: any, entropy: any): any {
  var stages: any = (((lineage !== null && typeof lineage === "object" && !Array.isArray(lineage) && !(lineage instanceof Set) && !(lineage instanceof Map))) ? py.get(lineage, "stages", []) : []);
  var steps: any = py.iter(stages).filter((s: any) => ((s !== null && typeof s === "object" && !Array.isArray(s) && !(s instanceof Set) && !(s instanceof Map)))).map((s: any) => py.get(s, "stage", py.toStr(s)));
  return {"evidence": py.sorted(py.toSet(py.iter(evidence).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e)))), "lineage_stages": steps, "uncertainty_basis": py.get(uncertainty, "deterministic_inputs", py.get(uncertainty, "factors", [])), "entropy": py.get(entropy, "entropy", 0), "explainable": true, "opaque": false, "deterministic_inputs": py.sorted(py.toSet(py.add(py.add([`evidence_count=${py.toStr(py.len(evidence))}`], [`stage_count=${py.toStr(py.len(steps))}`]), [...py.iter(py.or2(py.get(uncertainty, "deterministic_inputs", []), () => ([])))])))};
}
