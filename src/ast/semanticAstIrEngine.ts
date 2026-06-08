/**
 * Converted from Python: core/ast/semantic_ast_ir_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { parsePythonAst } from "./pythonAstEngine.js";
import { resolveSymbols } from "./symbolResolutionEngine.js";
import { buildControlFlowGraph } from "./controlFlowEngine.js";
import { reconstructExecutionPaths } from "./executionPathEngine.js";

export function compileSemanticAstIr(code: any): any {
  var ast_ir: any = parsePythonAst(code);
  var symbols: any = resolveSymbols(ast_ir);
  var cfg: any = buildControlFlowGraph(ast_ir);
  var execution_paths: any = reconstructExecutionPaths(cfg);
  return {"ast": ast_ir, "symbols": symbols, "control_flow_graph": cfg, "execution_paths": execution_paths, "semantic_grounded": true, "deterministic": true};
}
export { buildControlFlowGraph, parsePythonAst, reconstructExecutionPaths, resolveSymbols };
