/**
 * Converted from Python: core/graph/semantic_graph_validator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { checkGraphInvariants } from "./graphInvariantEngine.js";
import { validateSemanticEdge } from "./semanticEdgeValidationEngine.js";

export function validateSemanticGraph(graph: any): any {
  var inv: any = checkGraphInvariants(graph);
  var edge_results: any = py.iter(py.get(graph, "edges", [])).filter((e: any) => ((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))).map((e: any) => validateSemanticEdge(e));
  var invalid: any = py.enumerate(edge_results).filter(([i, r]: any) => !py.truthy(py.get(r, "valid"))).map(([i, r]: any) => i);
  return {"valid": py.and2(py.at(inv, "valid"), () => (!py.truthy(invalid))), "invariants": inv, "invalid_edges": invalid, "edge_count": py.len(edge_results), "deterministic_inputs": py.get(inv, "deterministic_inputs", [])};
}
export { checkGraphInvariants, validateSemanticEdge };
