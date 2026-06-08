/**
 * Converted from Python: core/memory/runtime_graph_memory_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeMemoryGraph(entities: any, relations: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var entity: any;
  for (entity of py.iter(py.slice(entities, null, 10000))) {
    var node_id: any = py.toStr(py.get(entity, "id", py.get(entity, "label", "")));
    if (!py.truthy(node_id)) {
      continue;
    }
    py.listAppend(nodes, {"id": node_id, "type": py.toStr(py.get(entity, "type", "entity"))});
  }
  var relation: any;
  for (relation of py.iter(py.slice(relations, null, 10000))) {
    py.listAppend(edges, {"from": py.toStr(py.get(relation, "from", "")), "to": py.toStr(py.get(relation, "to", "")), "relation": py.toStr(py.get(relation, "relation", "relates_to"))});
  }
  if (!py.truthy(nodes)) {
    py.listAppend(nodes, {"id": "memory:root", "type": "memory"});
  }
  return {"nodes": py.sorted(nodes, {key: ((item: any) => py.at(item, "id")) as (item: any) => any}), "edges": py.sorted(edges, {key: ((item: any) => [py.get(item, "from", ""), py.get(item, "to", ""), py.get(item, "relation", "")]) as (item: any) => any}), "bounded": true};
}
