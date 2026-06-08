/**
 * Converted from Python: core/memory/runtime_federation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function federateRuntimeMemory(memories: any): any {
  var federated_history: any[] = [];
  var federated_lineage: any[] = [];
  var federated_relations: any[] = [];
  var memory: any;
  for (memory of py.iter(memories)) {
    py.extend(federated_history, py.get(memory, "runtime_history", []));
    py.extend(federated_lineage, py.get(memory, "lineage", []));
    py.extend(federated_relations, py.get(memory, "semantic_relations", []));
  }
  return {"federated_count": py.len(memories), "runtime_history": py.sorted(federated_history, {key: ((item: any) => py.toInt(py.get(item, "tick", 0))) as (item: any) => any}), "lineage": py.sorted(federated_lineage, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "semantic_relations": py.sorted(federated_relations, {key: ((item: any) => [py.toStr(py.get(item, "from", "")), py.toStr(py.get(item, "to", ""))]) as (item: any) => any}), "bounded": true};
}
