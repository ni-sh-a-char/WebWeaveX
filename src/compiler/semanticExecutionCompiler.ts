/**
 * Converted from Python: core/compiler/semantic_execution_compiler.py
 * @generated — WebWeaveX python→javascript library port
 */

import { compileSemanticBytecode } from "../bytecode/index.js";

export function compileExecutionPlan(semantic_ir: any): any {
  var bytecode: any = compileSemanticBytecode(semantic_ir);
  return {"plan": bytecode, "compiled": true};
}
export { compileSemanticBytecode };
