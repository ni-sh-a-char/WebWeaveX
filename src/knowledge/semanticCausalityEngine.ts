/**
 * Converted from Python: core/knowledge/semantic_causality_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildOntology } from "./ontologyEngine.js";

export function reconstructKnowledgeCausality(entities: any, relations: any): any {
  var ont: any = buildOntology(entities, relations);
  var causal: any = py.iter(py.get(py.get(ont, "reconciled", {}), "relations", [])).map((r: any) => ({...(r), "relation": "depends_on", "evidence": py.get(r, "evidence", []), "lineage": py.get(r, "lineage", {})}));
  py.setItem(ont, "causal_dependencies", causal);
  return ont;
}
export { buildOntology };
