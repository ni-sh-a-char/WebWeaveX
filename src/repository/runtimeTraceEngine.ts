/**
 * Converted from Python: core/repository/runtime_trace_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelExecutionDependencies } from "./executionDependencyEngine.js";
import { parseSource } from "../parsers/parserRegistry.js";

export function traceRuntime(source: any, path: any = ""): any {
  var deps: any = modelExecutionDependencies(source, path);
  var parsed: any = (py.truthy(source) ? parseSource(source, path) : {});
  return {"trace": py.slice(py.get(deps, "edges", []), null, 100), "entrypoints": py.get(deps, "entrypoints", []), "language": py.get(parsed, "language", "text"), "evidence": py.get(deps, "evidence", [])};
}
export { modelExecutionDependencies, parseSource };
