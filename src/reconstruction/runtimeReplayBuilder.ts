/**
 * Converted from Python: core/reconstruction/runtime_replay_builder.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeReplay(actions: any = null, transactions: any = null, timeline: any = null, tick: any = 0): any {
  var ordered_actions: any = py.sorted(py.or2(actions, () => ([])), {key: ((item: any) => py.toStr(py.get(item, "id", py.get(item, "action_id", "")))) as (item: any) => any});
  var ordered_tx: any = py.sorted(py.or2(transactions, () => ([])), {key: ((item: any) => py.toStr(py.get(item, "transaction_id", ""))) as (item: any) => any});
  var chain: any = py.enumerate(ordered_actions).map(([index, action]: any) => ({"step": index, "action_id": py.toStr(py.get(action, "id", py.get(action, "action_id", ""))), "tick": py.add(tick, index)}));
  return {"replay_chains": chain, "execution_restoration": {"actions": ordered_actions, "transactions": ordered_tx}, "runtime_continuity": {"tick": tick, "steps": py.len(chain)}, "replay_package": {"actions": ordered_actions, "timeline": (py.truthy(timeline) ? py.get(timeline, "timeline", []) : []), "deterministic": true}, "bounded": true};
}
