/**
 * Converted from Python: core/repository/runtime_topology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { resolveRuntime } from "../parsers/runtimeResolutionEngine.js";

export function inferRuntimeTopology(dependencies: any, imports: any = null): any {
  var runtime: any = resolveRuntime(dependencies, py.or2(imports, () => ([])));
  return {"runtimes": py.get(runtime, "runtimes", []), "frameworks": py.get(runtime, "frameworks", []), "api_indicators": py.get(runtime, "api_indicators", []), "evidence": "parser_runtime_resolution"};
}
export { resolveRuntime };
