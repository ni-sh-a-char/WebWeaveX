/**
 * Converted from Python: core/knowledge/knowledge_reconstruction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildArchitectureKnowledge, buildConceptGraph, buildDependencyKnowledge, buildDocumentationKnowledge, buildRepositoryKnowledge, buildSemanticIdentity, resolveEntities } from "./reconstruction/index.js";

export function reconstructKnowledge(symbols: any = null, dependencies: any = null, documents: any = null): any {
  var sym: any = py.sorted(py.toSet(py.or2(symbols, () => ([]))));
  var deps: any = py.sorted(py.toSet(py.or2(dependencies, () => ([]))));
  var entities: any = resolveEntities(sym);
  var concept_graph: any = buildConceptGraph(sym);
  return {"entities": entities, "identity": buildSemanticIdentity(sym), "concept_graph": concept_graph, "repository": buildRepositoryKnowledge({"symbols": sym, "dependencies": deps}), "documentation": buildDocumentationKnowledge(py.or2(documents, () => ({}))), "architecture": buildArchitectureKnowledge({}), "dependencies": buildDependencyKnowledge(deps), "evidence_only": true};
}
export { buildArchitectureKnowledge, buildConceptGraph, buildDependencyKnowledge, buildDocumentationKnowledge, buildRepositoryKnowledge, buildSemanticIdentity, resolveEntities };
