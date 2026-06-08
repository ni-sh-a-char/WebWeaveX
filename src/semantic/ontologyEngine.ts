/**
 * Converted from Python: core/semantic/ontology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildSemanticOntology(entities: any, domain: any): any {
  var taxonomy: any = {"entity": py.sorted(py.toSet(py.iter(entities).map((e: any) => py.toStr(py.get(e, "type", ""))))), "runtime": ["browser", "native", "distributed", "application"], "workflow": ["transition", "submit", "navigate", "objective"], "ui": ["form", "dashboard", "navigation", "authentication"], "infrastructure": ["service", "api", "deployment", "monitoring"]};
  return {"entity_taxonomy": py.at(taxonomy, "entity"), "runtime_ontology": py.at(taxonomy, "runtime"), "workflow_ontology": py.at(taxonomy, "workflow"), "ui_ontology": py.at(taxonomy, "ui"), "infrastructure_ontology": py.at(taxonomy, "infrastructure"), "primary_domain": domain, "taxonomy": taxonomy, "bounded": true};
}
