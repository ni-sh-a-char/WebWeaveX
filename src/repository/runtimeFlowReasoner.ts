/**
 * Converted from Python: core/repository/runtime_flow_reasoner.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelExecutionDependencies } from "./executionDependencyEngine.js";
import { analyzeRuntimeSemantics } from "./runtimeSemanticsEngine.js";

export function reasonRuntimeFlow(source: any, path: any = "", files: any = null): any {
  var runtime: any = analyzeRuntimeSemantics(source, path);
  var exec_deps: any = modelExecutionDependencies(source, path);
  return {"runtime": runtime, "execution_flow": exec_deps, "topology": {"edges": py.get(exec_deps, "edges", [])}, "evidence": py.sorted(py.toSet(py.add(py.get(runtime, "evidence", []), py.get(exec_deps, "evidence", []))))};
}
export { analyzeRuntimeSemantics, modelExecutionDependencies };
