/**
 * Converted from Python: core/knowledge/civilization_ontology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelOntologyAlternatives } from "../evidence/ontologyAlternativeEngine.js";

export function applyCivilizationOntology(edge: any): any {
  var entities: any = [py.get(edge, "from", ""), py.get(edge, "to", "")];
  return {...(edge), "civilization_stability": {"plurality_preserved": true, "hardening_suppressed": true}, "ontology_alternatives": modelOntologyAlternatives(py.iter(entities).filter((e: any) => py.truthy(e)).map((e: any) => e))};
}
export { modelOntologyAlternatives };
