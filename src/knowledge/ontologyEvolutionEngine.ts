/**
 * Converted from Python: core/knowledge/ontology_evolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { evolveSemanticState } from "../memory/semanticEvolutionEngine.js";

export function evolveOntology(prior_edges: any, current_edges: any): any {
  var prior: any = {"relations": prior_edges, "version": py.len(prior_edges)};
  var current: any = {"relations": current_edges, "version": py.len(current_edges)};
  return evolveSemanticState(prior, current);
}
export { evolveSemanticState };
