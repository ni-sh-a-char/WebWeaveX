/**
 * Converted from Python: core/repository/runtime_semantics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { parseSource } from "../parsers/parserRegistry.js";
import { resolveRuntimeDependencies } from "./runtimeDependencyEngine.js";

export function analyzeRuntimeSemantics(source: any, path: any = ""): any {
  var parsed: any = (py.truthy(source) ? parseSource(source, path) : {});
  var deps: any = resolveRuntimeDependencies(parsed, source);
  var runtime: any = (py.truthy(parsed) ? py.get(parsed, "runtime", {}) : {});
  return {"dependencies": py.at(deps, "dependencies"), "runtime": runtime, "parser_first": py.get(deps, "parser_first", false), "evidence": py.get(deps, "evidence", []), "deterministic_inputs": py.get(py.get(parsed, "parser_grounding", {}), "deterministic_inputs", [])};
}
export { parseSource, resolveRuntimeDependencies };
