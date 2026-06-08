/**
 * Converted from Python: core/knowledge/ontology_evidence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function requireOntologyEvidence(edge: any): any {
  var ev: any = py.or2(py.get(edge, "evidence", []), () => ([]));
  if ((typeof ev === "string")) {
    ev = [ev];
  }
  var grounded: any = py.and2(py.truthy(ev), () => (!py.contains(edge, "type")));
  return {...(edge), "grounded": grounded, "evidence": py.sorted(py.toSet(py.iter(ev).map((e: any) => py.toStr(e)))), "grounding": py.get(edge, "grounding", {"method": (py.truthy(grounded) ? "evidence_backed" : "unsupported")}), "uncertainty": {"insufficient": !py.truthy(grounded)}};
}
