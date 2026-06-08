/**
 * Converted from Python: core/runtime/cluster_state_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function computeClusterState(nodes: any): any {
  return {"cluster_size": py.len(nodes), "node_ids": py.sorted(py.iter(nodes).filter((n: any) => (((n !== null && typeof n === "object" && !Array.isArray(n) && !(n instanceof Set) && !(n instanceof Map))) && py.truthy(py.get(n, "id")))).map((n: any) => py.get(n, "id")))};
}
