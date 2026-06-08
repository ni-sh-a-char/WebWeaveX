/**
 * Converted from Python: core/repository/dependency_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { resolveRuntimeDependencies } from "./runtimeDependencyEngine.js";
import { parseSource } from "../parsers/parserRegistry.js";

export function resolveRepositoryDependencies(source: any, path: any = ""): any {
  var parsed: any = (py.truthy(source) ? parseSource(source, path) : {});
  return resolveRuntimeDependencies(parsed, source);
}
export { parseSource, resolveRuntimeDependencies };
