/**
 * Converted from Python: core/ir/semantic_query_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let SemanticQueryIR: any = py.at(Object, [py.toStr, Object]);
export function compileSemanticQueryIr(query_type: any, target: any, result: any): any {
  return {"query_type": query_type, "target": target, "result": result, "evidence": py.get(result, "evidence", py.get(result, "semantic_evidence", {})), "explainable": true, "deterministic": true};
}
