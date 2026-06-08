/**
 * Converted from Python: core/repository/semantic_runtime_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildServiceRuntimeGraph } from "./serviceRuntimeGraphEngine.js";
import { modelExecutionDependencies } from "./executionDependencyEngine.js";

export function buildSemanticRuntimeGraph(source: any, path: any = "", files: any = null): any {
  var services: any = buildServiceRuntimeGraph(source, path, files);
  var deps: any = modelExecutionDependencies(source, path);
  return {"nodes": py.get(services, "nodes", []), "edges": py.add(py.get(services, "edges", []), py.get(deps, "edges", [])), "evidence": py.sorted(py.toSet(py.add(py.get(services, "evidence", []), py.get(deps, "evidence", []))))};
}
export { buildServiceRuntimeGraph, modelExecutionDependencies };
