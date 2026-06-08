/**
 * Converted from Python: core/repository/runtime_state_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { analyzeRuntimeExecution } from "./runtimeExecutionEngine.js";

export function modelRuntimeState(source: any, path: any = ""): any {
  var ex: any = analyzeRuntimeExecution(source, path);
  return {"state": (py.truthy(py.get(ex, "parser_backed")) ? "active" : "unknown"), "dependencies": py.get(py.get(ex, "runtime", {}), "dependencies", []), "execution": py.get(ex, "execution", {}), "evidence": py.get(ex, "evidence", []), "transitions": [{"from": "init", "to": (py.truthy(py.get(ex, "parser_backed")) ? "parsed" : "text")}]};
}
export { analyzeRuntimeExecution };
