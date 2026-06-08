/**
 * Converted from Python: core/reconstruction/runtime_state_rebuilder.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function rebuildRuntimeState(queues: any = null, synchronization: any = null, mutations: any = null, transactions: any = null, memory: any = null, execution_lineage: any = null, workflows: any = null): any {
  var ordered_mutations: any = py.sorted(py.or2(mutations, () => ([])), {key: ((item: any) => [py.toInt(py.get(item, "tick", 0)), py.toInt(py.get(item, "ordered_index", 0)), py.toStr(py.get(item, "kind", ""))]) as (item: any) => any});
  var ordered_transactions: any = py.sorted(py.or2(transactions, () => ([])), {key: ((item: any) => py.toStr(py.get(item, "transaction_id", ""))) as (item: any) => any});
  var ordered_queues: any = py.sorted(py.or2(queues, () => ([])), {key: ((item: any) => [(-py.toInt(py.get(item, "priority", 0))), py.toInt(py.get(item, "order", 0))]) as (item: any) => any});
  return {"queues": ordered_queues, "synchronization": py.pyDict(py.or2(synchronization, () => ({}))), "mutations": ordered_mutations, "transactions": ordered_transactions, "memory": py.pyDict(py.or2(memory, () => ({}))), "execution_lineage": py.sorted(py.or2(execution_lineage, () => ([])), {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "workflows": py.sorted(py.or2(workflows, () => ([])), {key: ((item: any) => py.toStr(py.get(item, "id", py.get(item, "objective", "")))) as (item: any) => any}), "deterministic_order": true, "bounded": true};
}
