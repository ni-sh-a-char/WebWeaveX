/**
 * Converted from Python: core/evidence/explainability_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildExplainability(parser_payload: any, confidence: any, provenance: any): any {
  var flags: Record<string, any> = {};
  if (((parser_payload !== null && typeof parser_payload === "object" && !Array.isArray(parser_payload) && !(parser_payload instanceof Set) && !(parser_payload instanceof Map)))) {
    flags = py.get(parser_payload, "parser_evidence", py.get(parser_payload, "evidence", {}));
    if (!((flags !== null && typeof flags === "object" && !Array.isArray(flags) && !(flags instanceof Set) && !(flags instanceof Map)))) {
      flags = {};
    }
  }
  var parser_basis: any = {"language": (py.truthy(parser_payload) ? py.get(parser_payload, "language", "text") : "unknown"), "flags": flags, "symbol_count": py.get(py.get(provenance, "grounding", {}), "symbol_count", 0)};
  var graph_basis: Record<string, any> = {};
  if ((py.truthy(parser_payload) && ((py.get(parser_payload, "semantic_graph") !== null && typeof py.get(parser_payload, "semantic_graph") === "object" && !Array.isArray(py.get(parser_payload, "semantic_graph")) && !(py.get(parser_payload, "semantic_graph") instanceof Set) && !(py.get(parser_payload, "semantic_graph") instanceof Map))))) {
    var g: any = py.at(parser_payload, "semantic_graph");
    graph_basis = {"nodes": py.len(py.or2(py.get(g, "nodes", []), () => ([]))), "edges": py.len(py.or2(py.get(g, "edges", []), () => ([])))};
  }
  var semantic_basis: any = {"confidence_score": py.get(confidence, "score", py.F(0.0)), "deterministic_inputs": py.get(confidence, "deterministic_inputs", [])};
  return {"parser_basis": parser_basis, "graph_basis": graph_basis, "semantic_basis": semantic_basis, "summary": py.sorted(py.or2(py.get(provenance, "evidence", []), () => ([])))};
}
