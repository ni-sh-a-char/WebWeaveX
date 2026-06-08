/**
 * Converted from Python: core/synchronization/runtime_consistency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function verifyRuntimeConsistency(history: any, convergence: any, replay: any): any {
  var deltas: any = [...py.iter(py.get(history, "deltas", []))];
  var issues: any[] = [];
  if (!py.truthy(py.get(convergence, "converged"))) {
    py.listAppend(issues, "convergence_incomplete");
  }
  if (!py.truthy(py.get(replay, "replayed"))) {
    py.listAppend(issues, "replay_not_ready");
  }
  var index: any;
  for (index = 1; index < py.len(deltas); index++) {
    if ((py.toInt(py.get(py.at(deltas, index), "timestamp", 0)) < py.toInt(py.get(py.at(deltas, py.sub(index, 1)), "timestamp", 0)))) {
      py.listAppend(issues, "timeline_order_violation");
      break;
    }
  }
  return {"consistent": py.eq(py.len(issues), 0), "issues": issues, "synchronization_integrity": py.eq(py.len(issues), 0), "semantic_continuity": py.contains(history, "semantic_evolution"), "replay_consistency": py.get(replay, "replayed", false), "distributed_convergence": py.get(convergence, "converged", false), "bounded": true};
}
