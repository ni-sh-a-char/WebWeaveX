import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";

/** Mirrors core.semantic.ontology_engine.build_semantic_ontology */
export function buildSemanticOntology(
  entities: Array<Record<string, unknown>>,
  domain: string,
): Record<string, unknown> {
  const taxonomy = {
    entity: [...new Set(entities.map((e) => String(e.type ?? "")))].filter(Boolean).sort(),
    runtime: ["browser", "native", "distributed", "application"],
    workflow: ["transition", "submit", "navigate", "objective"],
    ui: ["form", "dashboard", "navigation", "authentication"],
    infrastructure: ["service", "api", "deployment", "monitoring"],
  };
  return {
    entity_taxonomy: taxonomy.entity,
    runtime_ontology: taxonomy.runtime,
    workflow_ontology: taxonomy.workflow,
    ui_ontology: taxonomy.ui,
    infrastructure_ontology: taxonomy.infrastructure,
    primary_domain: domain,
    taxonomy,
    bounded: true,
  };
}

export function runOntologyRuntime(entities: Array<Record<string, unknown>>): Record<string, unknown> {
  const classes = new Set(entities.map((e) => String(e.type ?? "Entity")));
  return {
    ontology_id: computeDeterministicHash({ classes: [...classes].sort() }),
    classes: [...classes].sort(),
    entity_count: entities.length,
    bounded: true,
  };
}
