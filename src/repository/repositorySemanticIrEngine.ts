/**
 * Converted from Python: core/repository/repository_semantic_ir_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { resolveRuntimeDependencies } from "./runtimeDependencyEngine.js";
import { reconstructExecutionFlow } from "./executionFlowEngine.js";
import { inferServiceInteractions } from "./serviceInteractionEngine.js";
import { parseSource } from "../parsers/parserRegistry.js";

export function buildRepositorySemanticIr(source: any, path: any = "", files: any = null): any {
  var parsed: Record<string, any> = {};
  if (py.truthy(source)) {
    parsed = parseSource(source, path);
  }
  return {"language": py.get(parsed, "language", "text"), "symbols": py.get(parsed, "symbols", {}), "runtime_dependencies": resolveRuntimeDependencies(parsed, source), "execution_flow": reconstructExecutionFlow(parsed), "service_interactions": inferServiceInteractions(parsed, py.or2(files, () => ([]))), "parser_grounding": py.get(parsed, "parser_grounding", {}), "evidence": py.get(py.get(parsed, "parser_grounding", {}), "deterministic_inputs", [])};
}
export { inferServiceInteractions, parseSource, reconstructExecutionFlow, resolveRuntimeDependencies };
