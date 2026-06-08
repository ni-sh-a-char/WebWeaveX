/**
 * Converted from Python: core/ir/semantic_graph_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { proveGraphConsistency } from "../graph/graphConsistencyProver.js";
import { emptyConfidence, emptyLineage } from "./_base.js";

export let SemanticGraphIR: any = py.at(Object, [py.toStr, Object]);
export function compileSemanticGraphIr(graph: any): any {
  var proof: any = proveGraphConsistency(graph);
  return {"nodes": py.get(graph, "nodes", []), "edges": py.get(graph, "edges", []), "proof": proof, "lineage": emptyLineage("semantic_graph_ir"), "confidence": {"score": (py.truthy(py.get(proof, "proved")) ? py.F(1.0) : py.F(0.3)), "basis": py.get(proof, "deterministic_inputs", []), "deterministic": true}};
}
export { emptyConfidence, emptyLineage, proveGraphConsistency };
