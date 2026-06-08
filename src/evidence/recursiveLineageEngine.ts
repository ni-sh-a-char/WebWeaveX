/**
 * Converted from Python: core/evidence/recursive_lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function preserveRecursiveLineage(lineage: any, evidence: any, ambiguities: any, uncertainties: any, contradicted: any): any {
  var stages: any = (((lineage !== null && typeof lineage === "object" && !Array.isArray(lineage) && !(lineage instanceof Set) && !(lineage instanceof Map))) ? py.get(lineage, "stages", []) : []);
  var depth: any = ((Array.isArray(stages)) ? py.len(stages) : py.toInt(py.or2(py.get(lineage, "depth", 0), () => (0))));
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.get(contradicted, "pairs", []) : []);
  return {"depth": depth, "evidence_ancestry": [...py.iter(evidence)], "ambiguity_ancestry": [...py.iter(ambiguities)], "uncertainty_ancestry": [...py.iter(uncertainties)], "contradiction_ancestry": [...py.iter(pairs)], "entropy_ancestry_preserved": true, "instability_ancestry_preserved": true, "decay_prevented": true};
}
