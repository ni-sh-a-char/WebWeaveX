/**
 * Converted from Python: core/semantic/semantic_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let RELATION_MAP: any = {"organization": "owns", "service": "deploys", "api": "exposes", "metric": "monitors", "user": "authenticates", "workflow": "triggers", "infrastructure": "depends_on", "ui_action": "mutates"};
export function buildSemanticGraph(entities: any, relations: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var entity: any;
  for (entity of py.iter(py.slice(entities, null, 10000))) {
    var entity_type: any = py.toStr(py.get(entity, "type", "entity"));
    py.listAppend(nodes, {"id": py.toStr(py.get(entity, "id", "")), "type": entity_type, "label": py.toStr(py.get(entity, "label", ""))});
  }
  var relation: any;
  for (relation of py.iter(py.slice(relations, null, 10000))) {
    py.listAppend(edges, {"from": py.toStr(py.get(relation, "from", "")), "to": py.toStr(py.get(relation, "to", "")), "relation": py.toStr(py.get(relation, "relation", "related_to"))});
  }
  for (entity of py.iter(py.slice(entities, null, 10000))) {
    entity_type = py.toStr(py.get(entity, "type", ""));
    var mapped: any = py.get(RELATION_MAP, entity_type);
    if ((py.truthy(mapped) && (py.len(nodes) > 1))) {
      py.listAppend(edges, {"from": py.toStr(py.get(entity, "id", "")), "to": py.at(py.at(nodes, 0), "id"), "relation": mapped});
    }
  }
  if (!py.truthy(nodes)) {
    py.listAppend(nodes, {"id": "semantic:root", "type": "semantic"});
  }
  return {"nodes": py.sorted(nodes, {key: ((item: any) => py.at(item, "id")) as (item: any) => any}), "edges": py.sorted(edges, {key: ((item: any) => [py.get(item, "from", ""), py.get(item, "to", ""), py.get(item, "relation", "")]) as (item: any) => any}), "bounded": true};
}
