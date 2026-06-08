/**
 * Converted from Python: core/graph/semantic_topology_validator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { checkGraphInvariants } from "./graphInvariantEngine.js";

export function validateSemanticTopology(graph: any): any {
  var inv: any = checkGraphInvariants(graph);
  var edges: any = py.or2(py.get(graph, "edges", []), () => ([]));
  var grounded: any = py.sum(py.iter(edges).filter((e: any) => (((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map))) && py.truthy(py.get(e, "evidence")))).map((e: any) => 1));
  return {...(inv), "grounded_edges": grounded, "topology_valid": py.and2(py.at(inv, "valid"), () => (py.eq(grounded, py.len(edges))))};
}
export { checkGraphInvariants };
