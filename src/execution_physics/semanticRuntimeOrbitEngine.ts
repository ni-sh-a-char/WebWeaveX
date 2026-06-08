/**
 * Converted from Python: core/execution_physics/semantic_runtime_orbit_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_ORBITS: any = 1000;
export function computeRuntimeOrbits(runtime_ir: any): any {
  var topology: any = py.get(runtime_ir, "distributed_topology", {});
  var nodes: any = py.slice(py.sorted(py.get(topology, "nodes", []), {key: ((x: any) => py.toStr(py.get(x, "id"))) as (item: any) => any}), null, MAX_ORBITS);
  var orbits: any = py.enumerate(nodes).map(([idx, node]: any) => ({"orbit": idx, "node": py.get(node, "id")}));
  return {"orbits": orbits, "orbit_count": py.len(orbits), "bounded": true};
}
