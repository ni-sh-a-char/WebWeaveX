/**
 * Converted from Python: core/compiler/semantic_compiler_pipeline.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { lowerSemanticIr } from "./semanticLoweringEngine.js";
import { optimizeSemanticPipeline } from "./semanticOptimizationPipeline.js";
import { buildSemanticExecutionPlan } from "./semanticExecutionPlanner.js";
import { optimizeSemanticBytecode } from "./semanticBytecodeOptimizer.js";
import { compileSemanticBytecode } from "../bytecode/index.js";

export function compileSemanticPipeline(ir: any): any {
  var lowered: any = lowerSemanticIr(ir);
  var optimized: any = optimizeSemanticPipeline(lowered);
  var execution_plan: any = buildSemanticExecutionPlan(optimized);
  var bytecode_edges: any = {"edges": py.iter(py.get(optimized, "optimized_edges", [])).map((e: any) => ({"from": py.get(e, "source"), "to": py.get(e, "target")}))};
  var bytecode: any = compileSemanticBytecode(bytecode_edges);
  var instruction_dicts: any = py.iter(py.get(bytecode, "instructions", [])).map((ins: any) => ({"opcode": ins.opcode, "operand": ins.operand}));
  var bytecode_optimized: any = optimizeSemanticBytecode(instruction_dicts);
  return {"lowered_ir": lowered, "optimized_ir": optimized, "execution_plan": execution_plan, "bytecode": bytecode, "bytecode_optimized": bytecode_optimized};
}
export { buildSemanticExecutionPlan, compileSemanticBytecode, lowerSemanticIr, optimizeSemanticBytecode, optimizeSemanticPipeline };
