/**
 * Converted from Python: core/runtime/topology_runtime_convergence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function convergeRuntimeAndTopology(runtime_ir: any, topology_ir: any): any {
  var runtime_services: any = py.toSet(py.iter(py.get(py.get(runtime_ir, "distributed_topology", {}), "nodes", [])).map((n: any) => py.at(n, "id")));
  var topology_services: any = py.toSet(py.iter(py.get(topology_ir, "nodes", [])).map((n: any) => py.at(n, "id")));
  var aligned: any = py.sorted(py.bitand(runtime_services, topology_services));
  return {"aligned_services": aligned, "alignment_score": py.div(py.len(aligned), py.max([1, py.len(runtime_services)]))};
}
