/**
 * Converted from Python: core/engineering/semantic_runtime_drift_topology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeDriftTopology(current: any, baseline: any): any {
  var drift: any = py.sorted(py.bitxor(py.toSet(py.keys(current)), py.toSet(py.keys(baseline))));
  return {"drift_nodes": drift, "drift_count": py.len(drift)};
}
