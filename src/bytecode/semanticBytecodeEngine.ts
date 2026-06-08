/**
 * Converted from Python: core/bytecode/semantic_bytecode_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { SemanticInstruction } from "./semanticInstructionSet.js";

export let MAX_BYTECODE: any = 10000;
export function compileSemanticBytecode(semantic_ir: any): any {
  var instructions: any[] = [];
  var inner: any = py.get(semantic_ir, "optimized_ir", semantic_ir);
  var edges: any[] = [];
  if (((inner !== null && typeof inner === "object" && !Array.isArray(inner) && !(inner instanceof Set) && !(inner instanceof Map)))) {
    edges = [...py.iter(py.or2(py.get(inner, "edges", []), () => ([])))];
  }
  if (!py.truthy(edges)) {
    edges = [...py.iter(py.or2(py.get(semantic_ir, "edges", []), () => ([])))];
  }
  var edge: any;
  for (edge of py.iter(py.slice(edges, null, MAX_BYTECODE))) {
    py.listAppend(instructions, new SemanticInstruction("LINK", {"from": py.get(edge, "from"), "to": py.get(edge, "to")}));
  }
  return {"instructions": instructions, "count": py.len(instructions), "bounded": true};
}
export { SemanticInstruction };
