/**
 * Converted from Python: core/graph/graph_consistency_prover.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { assessGraphConsistency } from "./graphConsistencyEngine.js";
import { validateSemanticGraph } from "./semanticGraphValidator.js";

export function proveGraphConsistency(graph: any): any {
  var validation: any = validateSemanticGraph(graph);
  var consistency: any = assessGraphConsistency(graph);
  var proved: any = py.and2(py.at(validation, "valid"), () => (py.at(consistency, "consistent")));
  return {"proved": proved, "validation": validation, "consistency": consistency, "deterministic_inputs": py.get(validation, "deterministic_inputs", [])};
}
export { assessGraphConsistency, validateSemanticGraph };
