/**
 * Converted from Python: core/graph/graph_consistency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { checkGraphInvariants } from "./graphInvariantEngine.js";

export function assessGraphConsistency(graph: any): any {
  var inv: any = checkGraphInvariants(graph);
  return {"consistent": py.at(inv, "valid"), "invariants": inv, "deterministic_inputs": py.at(inv, "deterministic_inputs")};
}
export { checkGraphInvariants };
