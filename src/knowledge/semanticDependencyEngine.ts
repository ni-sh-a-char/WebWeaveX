/**
 * Converted from Python: core/knowledge/semantic_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildOntology } from "./ontologyEngine.js";

export function reconstructKnowledgeDependencies(entities: any, relations: any): any {
  var ont: any = buildOntology(entities, relations);
  var deps: any = py.iter(py.get(py.get(ont, "reconciled", {}), "relations", [])).map((r: any) => ({"from": py.at(r, "from"), "to": py.at(r, "to"), "evidence": py.get(r, "evidence", [])}));
  py.setItem(ont, "semantic_dependencies", deps);
  return ont;
}
export { buildOntology };
