/**
 * Converted from Python: core/repository/service_orchestration_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildSemanticRuntimeGraph } from "./semanticRuntimeGraphEngine.js";

export function modelServiceOrchestration(source: any, path: any = "", files: any = null): any {
  var graph: any = buildSemanticRuntimeGraph(source, path, files);
  return {"orchestration_graph": graph, "service_count": py.len(py.get(graph, "nodes", [])), "evidence": py.get(graph, "evidence", [])};
}
export { buildSemanticRuntimeGraph };
