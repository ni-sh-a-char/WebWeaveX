/**
 * Converted from Python: core/synchronization/runtime_history_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeHistory(deltas: any, transitions: any = null, workflows: any = null): any {
  transitions = py.or2(transitions, () => ([]));
  workflows = py.or2(workflows, () => ([]));
  return {"deltas": py.sorted(deltas, {key: ((item: any) => py.toInt(py.get(item, "timestamp", 0))) as (item: any) => any}), "transitions": transitions, "mutations": py.iter(deltas).flatMap((delta: any) => py.iter(py.get(delta, "changes", [])).map((change: any) => change)), "workflows": workflows, "semantic_evolution": py.iter(py.iter(deltas).flatMap((delta: any) => py.iter(py.get(delta, "changes", [])).map((change: any) => change))).filter((change: any) => py.eq(py.get(change, "kind"), "semantic_change")).map((change: any) => change), "length": py.len(deltas), "bounded": true};
}
