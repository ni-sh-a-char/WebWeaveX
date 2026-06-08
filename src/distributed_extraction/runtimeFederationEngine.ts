/**
 * Converted from Python: core/distributed_extraction/runtime_federation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildRuntimeGraph } from "../runtime_graph/runtimeGraphEngine.js";

export let MAX_RUNTIMES: any = 1000;
export function federateExtractionRuntimes(runtimes: any): any {
  var graphs: any[] = [];
  var runtime: any;
  for (runtime of py.iter(py.slice(runtimes, null, MAX_RUNTIMES))) {
    if ((py.truthy(py.get(runtime, "nodes")) || py.truthy(py.get(runtime, "edges")))) {
      py.listAppend(graphs, runtime);
    }
  }
  var merged: any = (py.truthy(graphs) ? buildRuntimeGraph(graphs) : {"ir": "unified_runtime_graph", "nodes": [], "edges": [], "bounded": true});
  return {"topology": merged, "runtime_count": py.len(py.slice(runtimes, null, MAX_RUNTIMES)), "bounded": true};
}
export { buildRuntimeGraph };
