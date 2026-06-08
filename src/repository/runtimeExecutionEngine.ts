/**
 * Converted from Python: core/repository/runtime_execution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { analyzeRuntimeSemantics } from "./runtimeSemanticsEngine.js";
import { reconstructExecutionFlow } from "./executionFlowEngine.js";
import { parseSource } from "../parsers/parserRegistry.js";

export function analyzeRuntimeExecution(source: any, path: any = ""): any {
  var parsed: any = (py.truthy(source) ? parseSource(source, path) : {});
  var runtime: any = analyzeRuntimeSemantics(source, path);
  var flow: any = reconstructExecutionFlow(parsed);
  return {"runtime": runtime, "execution": flow, "evidence": py.sorted(py.toSet(py.add(py.get(runtime, "evidence", []), py.get(flow, "evidence", [])))), "parser_backed": py.get(runtime, "parser_first", false)};
}
export { analyzeRuntimeSemantics, parseSource, reconstructExecutionFlow };
