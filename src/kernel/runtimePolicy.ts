/**
 * Converted from Python: core/kernel/runtime_policy.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildKernelPolicy(max_phases: any = 20, max_graph_nodes: any = 1000000, require_kaalka_persistence: any = true, allow_simulation: any = true): any {
  return {"max_phases": max_phases, "max_graph_nodes": max_graph_nodes, "require_kaalka_persistence": require_kaalka_persistence, "allow_simulation": allow_simulation, "deterministic": true, "bounded": true};
}
export function enforceKernelPolicy(policy: any, phase_count: any, node_count: any): any {
  var within_phases: any = (phase_count <= py.toInt(py.get(policy, "max_phases", 20)));
  var within_graph: any = (node_count <= py.toInt(py.get(policy, "max_graph_nodes", 1000000)));
  return {"allowed": py.and2(within_phases, () => (within_graph)), "within_bounds": py.and2(within_phases, () => (within_graph)), "bounded": true};
}
