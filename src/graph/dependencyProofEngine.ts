/**
 * Converted from Python: core/graph/dependency_proof_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function proveDependency(edge: any, evidence_required: any = true): any {
  var ev: any = py.or2(py.get(edge, "evidence", []), () => ([]));
  if ((typeof ev === "string")) {
    ev = [ev];
  }
  var proved: any = py.and2(py.truthy(py.get(edge, "from")), () => (py.and2(py.truthy(py.get(edge, "to")), () => ((py.truthy(evidence_required) ? py.truthy(ev) : true)))));
  return {"proved": proved, "from": py.get(edge, "from"), "to": py.get(edge, "to"), "evidence": py.sorted(py.toSet(py.iter(ev).map((e: any) => py.toStr(e)))), "justification": py.get(edge, "justification", {"rule": "dependency_requires_evidence"}), "uncertainty": py.get(edge, "uncertainty", {}), "deterministic_inputs": [`evidence=${py.toStr(py.len(ev))}`, `proved=${py.toStr(proved)}`]};
}
