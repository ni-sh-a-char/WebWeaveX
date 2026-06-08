/**
 * Converted from Python: core/engineering/semantic_runtime_diagnostics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_HEALTHY_GRAPH: any = 100000;
export function diagnoseSemanticRuntime(runtime_ir: any): any {
  var graph_db: any = py.get(runtime_ir, "graph_database", {});
  var graph_size: any = (((graph_db !== null && typeof graph_db === "object" && !Array.isArray(graph_db) && !(graph_db instanceof Set) && !(graph_db instanceof Map))) ? py.len(graph_db) : 0);
  var healthy: any = py.lt(graph_size, MAX_HEALTHY_GRAPH);
  return {"healthy": healthy, "graph_size": graph_size};
}
