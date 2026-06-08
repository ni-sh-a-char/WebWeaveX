/**
 * Converted from Python: core/execution/runtime_replay_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function replayRuntimeExecution(actions: any, transactions: any = null, mutations: any = null, tick: any = 0): any {
  var ordered_actions: any = py.sorted(actions, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any});
  var ordered_tx: any = py.sorted(py.or2(transactions, () => ([])), {key: ((item: any) => py.toStr(py.get(item, "transaction_id", ""))) as (item: any) => any});
  var ordered_mutations: any = py.sorted(py.or2(mutations, () => ([])), {key: ((item: any) => [py.toInt(py.get(item, "tick", 0)), py.toInt(py.get(item, "ordered_index", 0))]) as (item: any) => any});
  return {"actions": ordered_actions, "transactions": ordered_tx, "mutations": ordered_mutations, "tick": tick, "replayed": true, "identical": true, "bounded": true};
}
