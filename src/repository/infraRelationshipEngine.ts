/**
 * Converted from Python: core/repository/infra_relationship_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { detectInfraSignals } from "./infraSemanticEngine.js";

export function modelInfraRelationships(files: any): any {
  var signals: any = detectInfraSignals(files);
  var edges: any[] = [];
  var names: any = py.iter(py.get(signals, "signals", [])).map((s: any) => py.at(s, "file"));
  var i: any;
  for (i = 0; i < py.sub(py.len(names), 1); i++) {
    py.listAppend(edges, {"from": py.at(names, i), "to": py.at(names, py.add(i, 1)), "relation": "co_deployed", "evidence": ["infra:signal"]});
  }
  return {"signals": py.get(signals, "signals", []), "edges": edges, "evidence": py.get(signals, "evidence", [])};
}
export { detectInfraSignals };
