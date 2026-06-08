/**
 * Converted from Python: core/repository/runtime_dependency_propagation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { resolveRuntimeDependencies } from "./runtimeDependencyEngine.js";
import { parseSource } from "../parsers/parserRegistry.js";

export function propagateRuntimeDependencies(source: any, path: any = ""): any {
  var parsed: any = (py.truthy(source) ? parseSource(source, path) : {});
  var deps: any = resolveRuntimeDependencies(parsed, source);
  var propagated: any = py.iter(py.slice(py.get(deps, "dependencies", []), null, 100)).map((d: any) => ({"dep": d, "depth": 1}));
  return {"propagated": propagated, "evidence": py.get(deps, "evidence", []), "parser_first": py.get(deps, "parser_first")};
}
export { parseSource, resolveRuntimeDependencies };
