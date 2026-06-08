/**
 * Converted from Python: core/knowledge/entity_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { resolveSemanticIdentities } from "./semanticIdentityResolver.js";

export function resolveEntities(candidates: any, namespace: any = "ontology"): any {
  var ids: any = resolveSemanticIdentities(candidates, namespace);
  var clusters: Record<string, any> = {};
  var ent: any;
  for (ent of py.iter(py.get(ids, "entities", []))) {
    py.listAppend(py.setdefault(clusters, py.at(ent, "id"), []), py.at(ent, "name"));
  }
  return {"clusters": clusters, "entity_count": py.len(clusters), "evidence": ["ontology:identity_hash"]};
}
export { resolveSemanticIdentities };
