/**
 * Converted from Python: core/knowledge/ontology_entropy_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelOntologyEntropy(entities: any, edges: any): any {
  var n_ent: any = py.len(py.toSet(py.or2(entities, () => ([]))));
  var n_edge: any = py.len(py.or2(edges, () => ([])));
  var entropy: any = py.round(py.min([py.F(1.0), py.add(py.mul(n_ent, py.F(0.05)), py.mul(n_edge, py.F(0.03)))]), 3);
  return {"entropy": entropy, "entities": n_ent, "edges": n_edge, "deterministic_inputs": [`H=${py.floatStr(entropy)}`]};
}
